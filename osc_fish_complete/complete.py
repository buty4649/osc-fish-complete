import re

class CompleteFish:

    def __init__(self, name, output):
        self.name = str(name)
        self.output = output

    def write(self, cmdo, data):
        self.output.write("complete -c openstack -e\n")
        self.output.write(
            "complete -c openstack -f -n '__fish_is_first_token' -a '{0}'\n".format(cmdo))

        for subcommand, complete in data:
            subcommand = subcommand.replace('_', ' ')
            if complete.startswith("-"):
                for opt in complete.split(" "):
                    o = re.sub("^--", "", opt)
                    if opt.startswith("--"):
                        self.output.write(
                            "complete -c openstack -f -n '__fish_seen_subcommand_from {0}' -l '{1}'\n".format(subcommand, o))
                    else:
                        self.output.write(
                            "complete -c openstack -f -n '__fish_seen_subcommand_from {0}' -s '{1}'\n".format(subcommand, o))

        self.output.write("""
function __fish_openstack_complete
  set -l cmd (commandline -opc)
  switch "$cmd"
""")

        for subcommand, complete in data:
            if complete.startswith("-"):
                continue
            self.output.write("  case 'openstack {0}'\n".format(
                subcommand.replace("_", " ")))

            for c in complete.split(" "):
                self.output.write('    printf "{0}\\n"\n'.format(c))

        self.output.write("""end
end
complete -c openstack -x -a '(__fish_openstack_complete)'
""")
