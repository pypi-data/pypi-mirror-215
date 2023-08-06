# CMON_CLI_BEGIN

## autocomplete
function __fish_cmon_needs_command
  set cmd (commandline -opc)
  if [ (count $cmd) -eq 1 -a $cmd[1] = 'cmon' ]
    return 0
  end
  return 1
end

function __fish_cmon_using_command
  set cmd (commandline -opc)
  if [ (count $cmd) -gt 1 ]
    if [ $argv[1] = $cmd[2] ]
      return 0
    end
  end
  return 1
end

complete -f -c cmon -n '__fish_cmon_needs_command' -a '(cmon commands)'
for cmd in (cmon commands)
  complete -f -c cmon -n "__fish_cmon_using_command $cmd" -a \
    "(cmon completions (commandline -opc)[2..-1])"
end

# session-wise fix
ulimit -n 4096
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# CMON_CLI_END
