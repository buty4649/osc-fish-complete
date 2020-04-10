class CompleteFish:

  def __init__(self, name, output):
    self.name = str(name)
    self.output = output

  def write(self, cmdo, data):
    self.output.write("set -l openstack_command {0}\n".format(cmdo))
    self.output.write("""
function __fish_complete_openstack
  set -l cmd (commandline -opc)
  # HACK: Handle and/or/not specially because they have hardcoded completion behavior
  # that doesn't remove them from the commandline
  if contains -- $cmd[1] and or not
      set -e cmd[1]
  end
  set -e cmd[1]
  switch "$cmd"
""")
    for datum in data:
      self.output.write('    case "{0}"\n'.format(datum[0].replace('_', ' ')))
      self.output.write('      printf "%s\\n" {0}\n'.format(datum[1]))

    self.output.write("  end\n")
    self.output.write("end\n")
    self.output.write("complete -f -c openstack\n")
    self.output.write("complete -f -c openstack -a '(__fish_complete_openstack)'\n")
    self.output.write('complete -f -c openstack -n "not __fish_seen_subcommand_from {0}" -a "{0}"\n'.format(cmdo))
