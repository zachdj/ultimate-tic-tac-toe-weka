"""
This service provides a globally accessible source of information about the current application status
This can be used to, for example, cause a time-consuming method call to terminate early if the application is terminated
"""

terminated = False  # set to true by main.py when the app is exited