import json
import os
import requests
from enum import Enum

import docker as dockerpy

from .....settings.helpers import parse_boolean
from .....utils import milliseconds, nrlist, split_string
from ....mixins import DockerPy, IniLoader, StringIdentifier
from ...client import Oauth2FormatMany
from ..manage import ActorsCreate
from . import actorid

__all__ = ["ActorsManage"]

ENVS_FILE = "secrets.json"


class Stage(Enum):
    CONFIG = "config"
    BUILD = "build"
    PUSH = "push"
    CREATE = "create"


class WorkflowFailed(Exception):
    pass


class ActorsDeploy(Oauth2FormatMany, StringIdentifier, DockerPy, IniLoader):
    """Deploy an Actor from a project directory"""

    config = {}
    envs = {}
    dockerfile = None
    document = None
    results = []
    messages = []
    passed_vals = {}
    # TODO - make this user-specifiable
    working_dir = os.getcwd()

    # Workflow control flags
    build = True
    pull = True
    push = True
    create = True
    grant = True

    def get_parser(self, prog_name):

        parser = super(ActorsDeploy, self).get_parser(prog_name)
        parser = IniLoader.extend_parser(self, parser)
        parser = self.extend_parser(parser)
        return parser

    def extend_parser(self, parser):
        ig = parser.add_mutually_exclusive_group()
        # Update or force create
        ig.add_argument(
            "-I",
            "--id",
            dest="actor_id",
            type=str,
            help="Actor identifier (overrides existing)",
        )
        ig.add_argument(
            "--force-create",
            dest="force_create",
            action="store_true",
            help="Force creation of new Actor",
        )

        # Environment
        parser.add_argument(
            "-E",
            "--env-file",
            default=ENVS_FILE,
            dest="envs_file",
            help="Environment variables JSON file ({0})".format(ENVS_FILE),
        )

        # Workflow management
        parser.add_argument(
            "-R",
            "--dry-run",
            dest="workflow_dry_run",
            action="store_true",
            help="Shortcut: Only build container",
        )
        parser.add_argument(
            "--ignore-errors",
            dest="ignore_errors",
            action="store_true",
            help="Ignore deployment errors and warnings",
        )
        parser.add_argument(
            "--no-pull",
            dest="workflow_no_pull",
            action="store_false",
            help="Do not pull source image when building",
        )
        parser.add_argument(
            "--no-build",
            dest="workflow_no_build",
            action="store_false",
            help="Do not build container image",
        )
        parser.add_argument(
            "--no-push",
            dest="workflow_no_push",
            action="store_false",
            help="Do not push built container image",
        )
        parser.add_argument(
            "--no-create",
            dest="workflow_no_create",
            action="store_false",
            help="Do not create or update Tapis actor",
        )
        parser.add_argument(
            "--no-cache",
            dest="workflow_no_cache",
            action="store_false",
            help="Do not cache the Tapis actor identifer",
        )
        parser.add_argument(
            "--no-grant",
            dest="workflow_no_grant",
            action="store_false",
            help="Do not grant permissions after deployment",
        )

        return parser

    def log_message(self, stage: Enum, message):
        self.messages.append([stage.value, message])

    def get_configuration(self, parsed_args):
        config = self.get_ini_contents(parsed_args)
        if config == {}:
            raise WorkflowFailed("No project configuration file found")
        # Validate minimim viable configuration
        ACTOR_KEYS = ["name"]
        DOCKER_KEYS = ["namespace", "repo", "tag"]
        for k in ACTOR_KEYS:
            if config.get("actor", {}).get(k, None) is None:
                raise WorkflowFailed("actor#{0} missing from configuration".format(k))
            else:
                self.log_message(Stage.CONFIG, config.get("actor", {}).get(k))
        for k in DOCKER_KEYS:
            if config.get("docker", {}).get(k, None) is None:
                raise WorkflowFailed("docker#{0} missing from configuration".format(k))
            else:
                self.log_message(Stage.CONFIG, config.get("docker", {}).get(k))
        return config

    def configure_deployment_workflow(self, parsed_args):
        # Read workflow options
        self.build = parsed_args.workflow_no_build
        self.pull = parsed_args.workflow_no_pull
        self.push = parsed_args.workflow_no_push
        self.create = parsed_args.workflow_no_create
        self.docache = parsed_args.workflow_no_cache
        self.grant = parsed_args.workflow_no_grant
        self.ignore_errors = parsed_args.ignore_errors

        # Interpret --dry-run as a combination of workflow options
        if parsed_args.workflow_dry_run:
            self.build = True
            self.pull = True
            self.push = False
            self.create = False
            self.docache = False
            self.grant = False
            self.ignore_errors = False
            self.log_message(Stage.CONFIG, "Dry run requested")

        # if we don't build we should not push
        if self.build is False:
            self.push = False
            self.log_message(
                Stage.CONFIG, "Skipping push because no image will be built"
            )

    def get_dockerfile(self):
        """Compute path to application Dockerfile"""
        dockerfile = self.config.get("docker", {}).get("dockerfile", "Dockerfile")
        # TODO - Handle working directiory
        if not os.path.exists(dockerfile):
            raise FileNotFoundError("Dockerfile missing - project cannot be built")
        return dockerfile

    def take_action(self, parsed_args):

        # Init Tapis client
        self.load_client(parsed_args)
        # Configure Docker client
        self.docker_client_from_env()
        # Configure workflow
        self.configure_deployment_workflow(parsed_args)
        # Load configuration from ini file
        self.config = self.get_configuration(parsed_args)

        # Get Dockerfile
        self.dockerfile = self.get_dockerfile()
        self.log_message(Stage.CONFIG, "Dockerfile: {0}".format(self.dockerfile))

        # Accept actor_id from CLI first then from cache
        # WARNING: Can still be None if no identifier can be resolved
        if parsed_args.actor_id is not None:
            self.actor_id = parsed_args.actor_id
        else:
            self.actor_id = actorid.read_id()
        self.log_message(Stage.CONFIG, "actor_id: {0}".format(self.actor_id))

        # Read in environment vars from secrets.json
        try:
            self.envs = ActorsCreate.get_envs_from_file(
                parsed_args.envs_file, decryption_key=None
            )
            for k, _ in self.envs.items():
                self.log_message(Stage.CONFIG, "ENV found: {0}".format(k))
        except FileNotFoundError:
            pass

        try:
            self._build(parsed_args)
            self._push(parsed_args)
            self._create(parsed_args)
            self._docache(parsed_args)
            # self._grant(parsed_args)
        except Exception as exc:
            raise

        headers = ["stage", "message"]
        return (tuple(headers), tuple(self.messages))

    def _repo_tag(self):
        """Compute container repo:tag"""
        # Look for registry, default to empty
        registry = self.config.get("docker", {}).get("registry", None)
        if registry == "":
            registry = None
        # Handle registry in URL or hostname form
        if registry is not None:
            parsed_url = urllib.parse.urlparse(registry)
            if parsed_url.netloc != "":
                registry = parsed_url.netloc
            elif parsed_url.path != "":
                registry = parsed_url.path

        docker_conf = self.config.get("docker", {})

        # Look for namespace, then default to empty
        namespace = docker_conf.get(
            "organization",
            docker_conf.get("namespace", docker_conf.get("username", None)),
        )
        if namespace == "":
            namespace = None

        # Look for: docker.tag then default to empty
        tag = self.config.get("docker", {}).get("tag", None)
        if tag == "":
            tag = None

        # Look for docker.repo then default to empty
        repo = self.config.get("docker", {}).get("repo", None)
        if repo == "":
            repo = None
        if repo is None:
            raise WorkflowFailed("[docker]repo cannot be empty")

        if namespace is not None:
            # namespace/repo
            repo = namespace + "/" + repo
        if registry is not None:
            # registry/(namespace/?)repo
            repo = registry + "/" + repo
        if tag is not None:
            # (registry/?)(namespace/?)repo(:tag?)
            repo = repo + ":" + tag

        return repo

    def _dockerpy_test(self):
        try:
            self.dockerpy.images.list()
        except requests.exceptions.ConnectionError:
            raise SystemError(
                "Unable to communicate with Docker daemon. Is Docker installed and active?"
            )
        except Exception:
            raise

    def _build(self, parsed_args):
        """Build container"""
        if self.build:
            try:
                self._dockerpy_test()
                tag = self._repo_tag()
                dockerfile = self.get_dockerfile()
                self.log_message(Stage.BUILD, "Building {0}".format(tag))
                start_time = milliseconds()
                # TODO - build_args, labels, nocache, quiet, forcerm
                result = self.dockerpy.images.build(
                    path=self.working_dir,
                    tag=tag,
                    dockerfile=dockerfile,
                    pull=self.pull,
                    rm=True,
                )

                for log_line in result[1]:
                    txt = log_line.get("stream", "").strip()
                    if txt is not None and txt != "":
                        self.log_message(Stage.BUILD, log_line.get("stream", ""))

                self.log_message(
                    Stage.BUILD,
                    "Finished ({0} msec)".format(milliseconds() - start_time),
                )

                return True
            except Exception as err:
                if self.ignore_errors:
                    self.log_message(Stage.BUILD, str(err))
                    return False
                else:
                    raise

    def _push(self, parsed_args):
        """Push built container"""
        if self.push:
            try:
                self._dockerpy_test()
                tag = self._repo_tag()
                # print_stderr('Pushing {0}'.format(tag))
                self.log_message(Stage.BUILD, "Pushing {0}".format(tag))
                start_time = milliseconds()
                # TODO - auth_config
                for log_line in self.dockerpy.images.push(
                    tag, stream=True, decode=True
                ):
                    text_line = log_line.get("status", "").strip()
                    if text_line not in (
                        "Preparing",
                        "Waiting",
                        "Layer already exists",
                        "Pushing",
                        "Pushed",
                        "denied",
                    ):
                        self.log_message(Stage.BUILD, text_line)
                self.log_message(
                    Stage.BUILD,
                    "Finished ({0} msec)".format(milliseconds() - start_time),
                )
                # print_stderr('Finished ({} msec)'.format(milliseconds() -
                #  start_time))
                return True
            except Exception as err:
                if self.ignore_errors:
                    self.log_message(Stage.BUILD, str(err))
                    return False
                else:
                    raise

    def _create(self, parsed_args):
        """Create or update the actor"""
        if self.create:
            try:

                # Here, document is the configuration JSON that will be
                # sent to the actors endpoint. In create/update, we build it
                # directly, but to accomodate the more declarative form of using
                # the .ini file, we have to do a few things differently.
                # Specifically, we read in a ConfigParser object then extend and/
                # or modify it until it the resulting dict is shaped correctly
                # to configure an Actor.
                document = self.config["actor"]
                document["image"] = self._repo_tag()
                # Deploy ALWAYS forces an update to the actor
                document["force"] = True

                # Configure Actor's default environment as the right merge
                # of variables from project.ini[environment] and secrets.json
                # document['defaultEnvironment'] = self.envs
                union_envs = {**self.config["environment"], **self.envs}
                document["defaultEnvironment"] = union_envs

                # Configure Abaco cron from project.ini
                cron_schedule = document.pop("cron_schedule", None)
                cron_status = document.pop("cron_on", None)
                if cron_schedule is not None and cron_schedule != "":
                    document["cronSchedule"] = cron_schedule
                    # Override cron status via ini setting IF a schedule has been set
                    if cron_status is not None and cron_status != "":
                        document["cronOn"] = cron_status

                # Container UID
                cuid = document.pop("use_container_uid", None)
                if cuid is not None:
                    document["useContainerUid"] = parse_boolean(cuid)

                # Cast to booleans
                bool_keys = [
                    "privileged",
                    "stateless",
                    "token",
                    "useContainerUid",
                    "cronOn",
                ]
                for bk in bool_keys:
                    bkv = document.pop(bk, None)
                    if bkv is not None:
                        document[bk] = parse_boolean(bkv)

                if self.actor_id is None:
                    resp = self.tapis3_client.actors.create_actor(**document)
                    # resp = self.tapis_client.actors.add(body=document)
                    actor_id = resp.get("id", None)
                    setattr(self, "actor_id", actor_id)
                    self.log_message(Stage.CREATE, "Created Actor {0}".format(actor_id))

                else:
                    resp = self.tapis3_client.actors.update_actor(
                        actor_id=self.actor_id, **document
                    )
                    actor_id = resp.get("id", None)
                    setattr(self, "actor_id", actor_id)
                    self.log_message(Stage.CREATE, "Updated Actor {0}".format(actor_id))
                    # resp = self.tapis_client.actors.update(
                    #     actor_id=self.actor_id, body=document)

            except Exception as exc:
                if self.ignore_errors:
                    self.log_message(Stage.CREATE, str(exc))
                    return False
                else:
                    raise

    def _docache(self, parsed_args):
        """Cache the actor identifier"""
        if self.docache:
            actorid.write_id(self.actor_id)
            self.log_message(Stage.CREATE, "Cached actor_id to disk")
        return True
