Development mode: 
 - Make sure to pip uninstall serff-gen to make function navigation using ctrl + click or F12 scan within the workspace.
 - Run the script using python main.py
 - Observe lint and typing
 - Enable strict mode of Pylance extension
 - Enable isort extension run on save/autosave
 - Enable Black extension run on save/autosave

Sample CLI commands:
 - --generate project=my-project service=my-service runtime=python file=sample.yaml
    : Generates entire SERFF project in Python with modules created based on sample.yaml
 - --generate project=my-ts-project service=my-service runtime=typescript
    : Generates a clean SERFF project in TypeScript 
 - --add-module sample.yaml
    : Generates modules for an existing SERFF project

under construction..