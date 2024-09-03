
// CONSTANTS

/** The location of the file: vite.config.js, starting from root. */
const VITE_CONFIG_FILEPATH = "./client/vite.config.js";

/** The location of package.json, starting from root. */
const PACKAGE_JSON_FILEPATH = "./client/package.json";

/** The location of helpers.js, starting from root. */
const HELPERS_FILEPATH = "./client/src/helpers.js";

/** The location of configType.txt, starting from root. */
const CONFIG_TYPE_TXT_FILEPATH = "./configType.txt";

/** The backend url. */
const API_URL = "http://127.0.0.1:5000";

/** Line comment. */
const COMMENT_MARK = "// ";

/**
 * Constants representing the different route configuration types for this application.
 * 
 * Article of reference: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze
 */
const ConfigurationType = Object.freeze({
    /** Represents this application currently being developed and run locally. */
    DEVELOPMENT: "Development",
    /** Represents this application is live on the internet, and that anyone can access it now. */
    PRODUCTION: "Production"
});

/**
 * Throws an error message if, somehow an invalid configuration type was passed into the update functions.
 * Although, this should most likely not happen, as the user is restricted to selecting two options.
 * 
 * @param {*} configType 
 */
function invalidConfigTypeAlert(configType) {
    throw new Error("Route configuration failed! Invalid program mode detected!", configType);
}

/**
 * Adjusts the route settings on vite.config.js according to the desired configuration type.
 * 
 * If the developer is configuring for DEVELOPMENT, then the proxy key and value in the
 * file will be commented back in.
 * 
 * If the developer is configuring for PRODUCTION, then the proxy key and value in the file
 * will be commented out.
 * 
 * @param {fs} fs the file system.
 * @param {String} configType the configuration type.
 */
function updateViteConfig(fs, configType) {
    const data = fs.readFileSync(VITE_CONFIG_FILEPATH, "utf-8");
    const dataArr = data.split('\n');
    // console.log(dataArr);
    let configLineIndex = 0;
    let proxyCommentIndex;
    let addCommentColIndex;
    let loopCondition;
    let updateLineFunction;
    switch (configType) {
        case ConfigurationType.DEVELOPMENT:
            proxyCommentIndex = dataArr.indexOf("    // proxy: {");
            loopCondition = (index) => {
                return index < dataArr.length && dataArr[index].includes(COMMENT_MARK);
            } 
            addCommentColIndex = null;
            updateLineFunction = (line) => {
                const commentIndex = line.indexOf(COMMENT_MARK);
                return line.substring(0, commentIndex) + line.substring(commentIndex + COMMENT_MARK.length);
            }
            break;
        case ConfigurationType.PRODUCTION:
            proxyCommentIndex = dataArr.indexOf("    proxy: {");
            // Find the column index where the word proxy appears in the vite.config.js file.
            addCommentColIndex = proxyCommentIndex >= 0 ? dataArr[proxyCommentIndex].indexOf("proxy") : null;
            loopCondition = (index) => {
                return index < dataArr.length && dataArr[index].length >= addCommentColIndex;
            };
            updateLineFunction = (line) => {
                const newLine = line.substring(0, addCommentColIndex) + COMMENT_MARK + line.substring(addCommentColIndex);
                // console.log("New Line: ", newLine);
                return newLine;
            }
            break;
        default:
            invalidConfigTypeAlert();
            break;
    }
    if (proxyCommentIndex < 0) {
        console.log(`Routes are already configured for ${configType.toLowerCase()}!`);
        process.exit(0);
    }
    configLineIndex = proxyCommentIndex;
    while (loopCondition(configLineIndex)) {
        //console.log(configLineIndex);
        dataArr[configLineIndex] = updateLineFunction(dataArr[configLineIndex]);
        configLineIndex++;
    }
    const newViteConfig = dataArr.join('\n');
    fs.writeFileSync(VITE_CONFIG_FILEPATH, newViteConfig, "utf-8");
    // console.log("vite.config.js file updated successfully.");
}

/**
 * Adjusts the route settings on package.json according to the desired configuration type.
 * 
 * If the developer is configuring for DEVELOPMENT, then the proxy key and value in the
 * file will be removed.
 * 
 * If the developer is configuring for PRODUCTION, then the proxy key and value, which is
 * the API URL, will be added back in.
 * 
 * @param {fs} fs the file system.
 * @param {String} configType the configuration type.
 */
function updatePackageJSON(fs, configType) {
    const data = fs.readFileSync(PACKAGE_JSON_FILEPATH, 'utf-8');
    const pkgJson = JSON.parse(data);
    switch (configType) {
        case ConfigurationType.DEVELOPMENT:
            delete pkgJson.proxy;
            break;
        case ConfigurationType.PRODUCTION:
            pkgJson.proxy = API_URL;
            break;
        default:
            invalidConfigTypeAlert();
            break;
    }
    fs.writeFileSync(PACKAGE_JSON_FILEPATH, JSON.stringify(pkgJson, null, 2), 'utf-8');
    // console.log('Package.json file updated successfully!');
}


/**
 * Adjusts the route settings on helpers.js according to the desired configuration type.
 * 
 * If the developer is configuring for DEVELOPMENT, then the routePrefix constant will be
 * set to "/api".
 * 
 * If the developer is configuring for PRODUCTION, then the routePrefix constant will be
 * set to an empty string.
 * 
 * @param {fs} fs the file system.
 * @param {String} configType the configuration type.
 */
function updateHelpers(fs, configType) {
    const data = fs.readFileSync(HELPERS_FILEPATH, "utf-8");
    let newRoutePrefix;
    switch (configType) {
        case ConfigurationType.DEVELOPMENT:
            newRoutePrefix = "\"/api\"";
            break;
        case ConfigurationType.PRODUCTION:
            newRoutePrefix = "\"\"";
            break;
        default:
            invalidConfigTypeAlert();
    }

    const dataArr = data.split('\n');
    for (let lineIndex = 0; lineIndex < dataArr.length; lineIndex++) {
        // console.log(lineIndex);
        if (dataArr[lineIndex].includes("const routePrefix")) {
            dataArr[lineIndex] = `const routePrefix = ${newRoutePrefix};`;
            break;
        }
    }

    const updatedHelperData = dataArr.join('\n');
    fs.writeFileSync(HELPERS_FILEPATH, updatedHelperData, "utf-8");
    // console.log("helpers.js file updated successfully.");
}

/**
 * Adjusts the route settings on configType.txt according to the desired configuration type.
 * This file only contains a single line, indicating the target configuration type.
 * It should not contain anything else.
 * 
 * @param {fs} fs the file system.
 * @param {String} configType the configuration type.
 */
function updateConfigTypeTxt(fs, configType) {
    let data = fs.readFileSync(CONFIG_TYPE_TXT_FILEPATH, "utf-8");
    data=configType;
    fs.writeFileSync("./configType.txt", data, "utf-8");
    // console.log("configType.txt file updated successfully.");
}

/**
 * Configures route settings on the front end.
 * First, it will update the vite.config.js file.
 * Then, it will update the package.json file.
 * Finally, it will update the helpers.js file.
 * 
 * References below:
 * 
 * @see
 * https://stackoverflow.com/questions/10685998/how-to-update-a-value-in-a-json-file-and-save-it-through-node-js
 * https://stackoverflow.com/questions/62225160/how-can-i-modify-a-js-file-and-save-it-with-an-npm-command
 * https://www.geeksforgeeks.org/node-js-fs-writefile-method/
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse
 * 
 * 
 * @param {String} configType the configuration type.
 */
function configureRoutes(configType) {
    const fs = require('fs');
    updateViteConfig(fs, configType);
    updatePackageJSON(fs, configType);
    updateHelpers(fs, configType);
    updateConfigTypeTxt(fs, configType);
    console.log(`Routes have been configured for ${configType}!`);
    return true;
}

/**
 * Menu for developers to select the appropriate configuration type.
 * Selecting Development will configure route settings so that you can test this application on a development environment.
 * Selecting Production will configure route settings so that you can deploy this application and run it live.
 * 
 * References below:
 * 
 * @see
 * https://www.npmjs.com/package/inquirer
 * https://stackoverflow.com/questions/58442756/nodejs-how-to-re-display-custom-cli-menu-after-executing-corresponding-function
 */
const inquirer = require('inquirer');
const configMenu = () => {
    inquirer.prompt([
        {
            name: 'configType',
            type: 'list',
            message: 'Select the configuration type: ',
            choices: ['Development', 'Production']
        }
    ]).then((answers) => {
        return configureRoutes(answers.configType);
    }).catch((error) => {
        console.error(error);
    });
}

configMenu();