from dataclasses import dataclass

from colorama import Fore as f


@dataclass
class Command:
    CMD: str
    argv: list[str]

    def __repr__(self):
        return f"<cmd: {self.CMD}, args: {self.arg_str} arglen: {len(self.argv)}>"

    @property
    def arg_str(self) -> str:
        return " ,".join([f"{i}\n" for i in self.argv])


class Shell:
    """A basic shell out of the box."""

    def shellInput(self, Tool: str = None) -> Command | bool:
        """Gets User input then returns a parsed command."""
        if Tool:
            re_val = self.parseCmd(
                input(f"  {f.YELLOW}[*][{Tool}] {f.CYAN}-> {f.WHITE}")
            )
            if re_val:
                return re_val
            else:
                return False
        else:
            re_val = self.parseCmd(input(f"  {f.YELLOW}[*] {f.CYAN}-> {f.WHITE}"))
            if re_val:
                return re_val
            else:
                return False

    def parseCmd(self, cmd: str) -> Command | bool:
        """Parses a command and returns the command and its args."""
        if len(cmd) > 0:
            if len(cmd.split(" ")) > 1:
                return Command(
                    cmd.split(" ")[0].strip().upper(),
                    [i.strip() for i in cmd.split(" ")[1:]],
                )
            else:
                return Command(cmd.split(" ")[0].strip().upper(), [])
        else:
            return False
