
import os
import platform

import click
from .device_client_constants import ClientConstants
from .device_client_runner import FedMLClientRunner


def login_with_docker_mode(userid, version, docker_rank):
    account_id = userid

    # Get os name
    sys_name = platform.system()
    if sys_name == "Darwin":
        sys_name = "MacOS"

    # Get data directory
    cur_dir = ClientConstants.get_fedml_home_dir()

    # Set default version if the version argument is empty
    if version == "":
        version = "release"

    # Set registry server and image path based on the version.
    if version == "dev":
        image_dir = "/x6k8q1x9"
    elif version == "release":
        image_dir = "/x6k8q1x9"
    elif version == "test":
        image_dir = "/s8w2q1c1"
    registry_server = "public.ecr.aws"

    # Set image tags based on the version
    tag = version

    # Set client agent image path and client image path
    client_image_name = "fedml-client-agent:" + tag
    image_path = image_dir + "/" + client_image_name
    client_agent_image = registry_server + image_path

    # Get device id based on your machine MAC address.
    os_name = sys_name
    device_id = "{}@Rank{}".format(FedMLClientRunner.get_device_id(), str(docker_rank))

    # Set environment variables for client agent docker
    env_account_id = account_id
    env_version = version
    env_current_running_dir = cur_dir
    env_current_os_name = os_name
    env_current_device_id = device_id

    # Cleanup the running docker
    click.echo("Your FedML client agent is being deployed, please wait for a moment...")

    # Pull client agent docker
    fedml_docker_name = "fedml_client_agent_{}".format(str(docker_rank))
    click.echo("Now is pulling fedml docker client.........................")
    os.system("docker pull " + client_agent_image)
    click.echo("Now is opening fedml docker client.........................")
    docker_stop_proc = ClientConstants.exec_console_with_shell_script_list(['docker', 'stop', fedml_docker_name])
    _, _, _ = ClientConstants.get_console_pipe_out_err_results(docker_stop_proc)
    docker_rm_proc = ClientConstants.exec_console_with_shell_script_list(['docker', 'rm', fedml_docker_name])
    _, _, _ = ClientConstants.get_console_pipe_out_err_results(docker_rm_proc)

    # Compose the command for running the client agent docker
    fedml_client_home_dir = os.path.join(env_current_running_dir, "docker", "rank-"+str(docker_rank))
    try:
        os.makedirs(fedml_client_home_dir)
    except:
        pass
    docker_run_cmd = "docker run --name " + fedml_docker_name + \
                     " -v " + fedml_client_home_dir + ":/home/fedml/fedml-client" + \
                     " --env ACCOUNT_ID=" + str(env_account_id) + \
                     " --env FEDML_VERSION=" + env_version + \
                     " --env CLIENT_DEVICE_ID=" + env_current_device_id + \
                     " --env CLIENT_OS_NAME=" + env_current_os_name + \
                     " -d " + client_agent_image

    # Run the client agent docker
    os.system(docker_run_cmd)

    # Get the running state for the client agent docker
    docker_ps_process = ClientConstants.exec_console_with_shell_script_list(['docker', 'ps', '-a'],
                                                                            should_capture_stdout_err=True)
    ret_code, out, err = ClientConstants.get_console_pipe_out_err_results(docker_ps_process)
    is_deployment_ok = False
    if out is not None:
        out_str = out.decode(encoding="utf-8")
        if str(out_str).find(fedml_docker_name) != -1 and str(out_str).find("Up") != -1:
            is_deployment_ok = True
    if err is not None:
        err_str = err.decode(encoding="utf-8")
        if str(err_str).find(fedml_docker_name) != -1 and str(err_str).find("Up") != -1:
            is_deployment_ok = True

    if is_deployment_ok:
        print("\n\nCongratulations, your device is connected to the FedML MLOps platform successfully!")
        print(
            "Your unique device ID is "
            + str(env_current_device_id)
            + "\n"
        )
        
        logs_with_docker_mode(docker_rank)
    else:
        click.echo("Oops, you failed to deploy the FedML client agent.")
        click.echo("Please check whether your Docker Application is installed and running normally!")


def logout_with_docker_mode(docker_rank):
    fedml_docker_name = "fedml_client_agent_{}".format(str(docker_rank))
    click.echo("Logout.........................")
    os.system("docker stop {}".format(fedml_docker_name))
    os.system("docker rm {}".format(fedml_docker_name))


def logs_with_docker_mode(docker_rank):
    fedml_docker_name = "fedml_client_agent_{}".format(str(docker_rank))
    docker_name_format = 'name={}'.format(fedml_docker_name)
    docker_name_proc = ClientConstants.exec_console_with_shell_script_list(['docker', 'ps', '-aqf', docker_name_format],
                                                                           should_capture_stdout_err=True)
    _, out_id, err_id = ClientConstants.get_console_pipe_out_err_results(docker_name_proc)
    if out_id is not None:
        out_id_str = out_id.decode(encoding="utf-8")
        docker_logs_cmd = 'docker logs -f {}'.format(out_id_str)
        os.system(docker_logs_cmd)


if __name__ == "__main__":
    login_with_docker_mode("214", "dev", 1)
    #logout_with_docker_mode(1)

