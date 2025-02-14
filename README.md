> Note: This is Auzuma Technologies's **FIRST** automation tool! Please be patient, and please enjoy!
# lambda-automationWithConfig (LAWC) automation tool

LAWC is an automation command-line tool written in Python that uses a JSON configuration file to set up a Lambda function. It modifies a template Lambda function by replacing placeholders with actual values from the JSON config file, matching the user’s desired configuration.

# How it works

LAWC requires a template Lambda function folder as input. This folder serves as the base for the Lambda function the user wants to configure. The template contains all the necessary files, but the files are filled with placeholders instead of real values for things like function names and keys. For example, a placeholder might look like `LambdaFunctionName`.

The tool’s goal is to automatically replace all placeholders in the input template Lambda with actual values from the user's JSON config file. This automates the process, saving the user from manually searching and replacing (Ctrl+F Replace) each placeholder in their template via a standard editor.

### Example configuration file

Your JSON configuration file should map placeholder keys to their intended values. Here's an example:

```json
{
    "LambdaFunctionName": "MyLambdaFunction",  // Assuming the user's placeholder in the input template is LambdaFunctionName
    "Lambda Function Description": "My Lambda Function",  // Assuming the user's placeholder in the input template is LambdaFunctionDescription
    "esiOAuthSecretName": "esi/myLambda/oauth",  // Assuming the user's placeholder in the input template is esiOAuthSecretName
    "clientAuthSecretName": "jaas/myLambda/oauth",  // Assuming the user's placeholder in the input template is jaasOAuthSecretName
    "consumerInterfaceKey": "myLambda_consumer"  // Assuming the user's placeholder in the input template is consumerInterfaceKey

    // ... and so on for other placeholders

    "file_name_maps (Special Property)": { // This is the exact name of the property
        "MyPlaceholderFile.ts": "MyConfiguredFile.ts", // Assuming the user's placeholder file name in the input template is MyPlaceholderFile.ts, and the user wants to save the configured file as MyConfiguredFile.ts
        "types/MyPlaceholderTypes.d.ts": "types/MyConfiguredTypes.d.ts" // Assuming the user's placeholder file name in the input template is in types/MyPlaceholderTypes.d.ts, and the user wants to save the configured file as types/MyConfiguredTypes.d.ts
    }
}
```

Each key in this configuration corresponds to a placeholder in your template files. When LAWC processes your template, it replaces each placeholder with its corresponding value from the configuration file, creating a fully configured Lambda function in seconds.

The tool's main advantage is its ability to perform all replacements automatically, saving you from the tedious process of manually updating each placeholder through a standard text editor's find-and-replace function.

# How to run

Since LAWC is a comand-line tool, it should be run like this:

```bash
python lawc.py
```

It will then prompt the user, `input()`-by-`input()`, for the following:

1. The absolute path to the template Lambda function folder. (If the folder is not found, or if the folder is empty, the tool will raise a user-freindly error and exit immediately.)
2. The absolute path to the JSON configuration file. (If the JSON file is not found, or if the content of the JSON file ain't valid, the tool will raise a user-freindly error and exit immediately.)
3. The absolute path to the destination folder, where the fully configured, no-placeholder-left-behind Lambda function will be saved.
