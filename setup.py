import cx_Freeze

executables = [cx_Freeze.Executable("COVID19 Game.py")]

cx_Freeze.setup(
    name="covid19",
    options={"build_exe": {"packages":["pygame"]}},
    executables = executables

    )
