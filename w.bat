@echo off
::
if "%1"=="" (
    set /P first_param="Type in the first_param."
) else (
    set first_param=%1
)
::
if "%first_param%"=="n" goto :nutrition
goto :finish
::
:nutrition_loop
    python %~dp0\nutrition
    timeout 3 > nul
    goto :nutrition_loop

:try_install_global_python
    if exist "%python_3_6_15%" (
        echo The %python_3_6_15% was existed.
    ) else (
        echo The python_3_6_15 was not existed.
        %~dp0\external_dependencies\python-3.6.15-amd64.exe /passive /repair
        %~dp0\external_dependencies\python-3.6.15-amd64.exe /passive /uninstall
        rmdir /S /Q %~dp0\python_3_6_15
        mkdir %~dp0\python_3_6_15
        %~dp0\external_dependencies\python-3.6.15-amd64.exe /passive TargetDir=%~dp0\python_3_6_15
        setx python_3_6_15 %~dp0\python_3_6_15\python.exe
    )
    exit /B 0

:try_install_venv_nutrition
    if exist "%~dp0\nutrition\venv\Scripts\python.exe" (
        echo The %~dp0\nutrition\venv\Scripts\python.exe was existed.
    ) else (
        echo The %~dp0\nutrition\venv\Scripts\python.exe was not existed.
        %python_3_6_15% -m venv %~dp0\nutrition\venv --clear
        %~dp0\nutrition\venv\Scripts\python.exe -m pip install -r %~dp0\nutrition\confs\requirements.txt --proxy=http://pxbud.evosoft.com:8080
        %~dp0\nutrition\venv\Scripts\python.exe -m pip install -r %~dp0\nutrition\confs\requirements.txt
    )
    exit /B 0

:nutrition_ci
    call %~dp0\nutrition\venv\Scripts\activate.bat
    %~dp0\nutrition\venv\Scripts\black.exe %~dp0\nutrition --config %~dp0\nutrition\confs\pyproject.toml
    call %~dp0\nutrition\venv\Scripts\deactivate.bat
    exit /B 0

:nutrition
    call :try_install_global_python
    call :try_install_venv_nutrition
    call :nutrition_ci
    call :nutrition_loop
:finish
    echo Finished!