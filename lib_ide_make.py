# BuildFox ninja generator

import os, sys

def gen_make(buildfox_name, cmd_env, ninja_gen_mode, filename = "Makefile"):
	text = """# generated by BuildFox
%s
compile:
	ninja
clean:
	ninja -t clean
"""

	if ninja_gen_mode:
		all = "all: compile"
	else:
		if cmd_env:
			all = "all: set_env configure compile\n"
			all += "set_env:\n"
			all += "\t%s\n" % cmd_env.replace("#", "\\#").replace("$", "$$")
		else:
			all = "all: configure compile\n"

		bf_exec = os.path.abspath(sys.argv[0])
		if bf_exec.endswith(".py"):
			bf_exec = sys.executable + " " + bf_exec
		bf_cmd = bf_exec + " --just-generate"
		if buildfox_name != "build.fox":
			bf_cmd += " -i " + buildfox_name
		all += "configure:\n"
		all += "\t%s" % bf_cmd

	with open(filename, "w") as f:
		f.write(text % all)
