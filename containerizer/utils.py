from typing import List, Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from .types import Options



convert_to_list_args = lambda x: x.split(" ") if x else []


def process_build_args(options: "Options", processer: Callable):
    assert (
        options.build_commands is not None
    ), f"No build commands provided, please add a default for {options.framework}"
    for cmd in options.build_commands:
        cmd = processer(cmd)

    cmds = ""
    cmds += f"RUN {convert_list(options.build_commands)}\n"

    return cmds




def convert_list(list_cmds: List):
    return " && ".join(list_cmds)


