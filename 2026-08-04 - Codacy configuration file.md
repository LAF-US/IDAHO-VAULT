---
title: "Codacy configuration file"
source: "https://docs.codacy.com/repositories-configure/codacy-configuration-file/"
author:
  - "[[support@codacy.com (Codacy Support)]]"
published: 2026-08-04
created: 2026-08-13
description: "Use the Codacy configuration file to configure advanced features on Codacy with more control such as ignoring files for duplication or a specific tool, configuring the root directory to start the analysis, and adding custom file extensions to languages."
---
Codacy supports configuring certain advanced features through a configuration file, such as:

## Using a Codacy configuration file

> [!important] Important
> - If your repository has a Codacy configuration file, the [Ignored files settings](https://docs.codacy.com/repositories-configure/ignoring-files/) defined on the Codacy UI don't apply and you must [ignore files using the configuration file](#syntax-for-ignoring-files) instead.
> - Codacy always uses the configuration file **in the default branch**. New settings added to the Codacy configuration file by a pull request are also considered for the pull request analysis, but the existing configuration in the default branch takes precedence.
> 	For example, if a pull request removes an ignored path from the Codacy configuration file, any matching files will stay ignored until that pull request is merged into the default branch.

To use a Codacy configuration file:

1. Create a text file with the name `.codacy.yml` or `.codacy.yaml` on the root of your repository.
	The file must start with a line containing a triple dash (`---`).
2. Add your settings to the configuration file based on the example template below.
	If you defined any [Ignored files settings](https://docs.codacy.com/repositories-configure/ignoring-files/) for the repository, make sure you [add those settings](#syntax-for-ignoring-files) to the Codacy configuration file.
	```js
	---
	engines:
	  rubocop:
	    exclude_paths:
	      - "config/test.yml"
	    base_sub_dir: "test/baseDir"
	  duplication:
	    exclude_paths:
	      - "config/test.yml"
	    config:
	      languages:
	        - "ruby"
	  metric:
	    exclude_paths:
	      - "src/test.ts"
	    config:
	      languages:
	        - "typescript"
	languages:
	  css:
	    extensions:
	      - ".scss"
	  python:
	    enabled: false
	exclude_paths:
	  - ".bundle/**"
	  - "spec/**/*"
	  - "benchmarks/**/*"
	  - "**.min.js"
	  - "**/tests/**"
	include_paths:
	  - "**/tests/integration/**"
	```
3. Optionally, validate the syntax of your configuration file with the [Codacy Analysis CLI](https://github.com/codacy/codacy-analysis-cli#install) by running the following command in the same folder as the Codacy configuration file:
	```js
	codacy-analysis-cli validate-configuration --directory \`pwd\`
	```

## Ignoring files using a Codacy configuration file

The Codacy configuration file gives you more flexibility in [ignoring or excluding files](https://docs.codacy.com/repositories-configure/ignoring-files/) from the Codacy analysis.

> [!note] Note
> To exclude files from coverage analysis only, you must ignore them directly in the tool you're using to generate coverage reports and ensure that the reports you upload to Codacy don't include coverage information for those files.

### Syntax for ignoring files

To ignore files using a Codacy configuration file, you must define one or more patterns under `exclude_paths` using the [Java glob syntax](https://docs.oracle.com/javase/7/docs/api/java/nio/file/FileSystem.html#getPathMatcher%28java.lang.String%29):

| Example pattern | Ignored files |
| --- | --- |
| `test/README.md` | The file `test/README.md` |
| `test/*` | All files in the root of test |
| `test/**` | All files and directories inside test |
| `test/**/*` | All files inside sub-directories of test |
| `**.resource` | All `.resource` files across all your repository |
| `**/*.resource` | All `.resource` files in all directories and sub-directories |

For example:

```js
---
exclude_paths:
  - "test/README.md"
  - "**/*.resource"
```

### Syntax for configuring cyclomatic complexity

Cyclomatic complexity can be disabled or partially ignored for certain paths, files or languages.

> [!note] Note
> Cyclomatic complexity is referred as `metric` in the configuration file.
> 
> ```js
> ---
> engines:
>   metric:
>     exclude_paths:
>       - "src/test.ts"
>     config:
>       languages:
>         - "typescript"
> ```

## Including specific files using a Codacy configuration file

The Codacy configuration file allows you to explicitly specify files or directories to include in the analysis. This is particularly useful for [bypassing files or directories that are ignored by default](https://docs.codacy.com/repositories-configure/ignoring-files/#default-ignored-files) or specified in `exclude_paths`.

> [!note] Note
> If both `exclude_paths` and `include_paths` are defined, `include_paths` will specify exceptions to the exclusions defined in `exclude_paths`.

### Syntax for including files

To include specific files using a Codacy configuration file, you must define one or more patterns under `include_paths` [using the same syntax as `exclude_paths`](#syntax-for-ignoring-files).

For example:

```js
---
exclude_paths:
  - "lib*/**"
include_paths:
  - "lib-a/**"
  - "libs/**"
```

In this example, while all directories matching `lib*` are excluded, `lib-a` is specifically included for analysis, as well as any files within `libs`.

## Adjusting tool configurations

> [!note] Note
> The Codacy configuration file lets you [configure tools](#tool-specific-configurations), but you can't enable or disable them. A tool can only be enabled or disabled on the [Code patterns page](https://docs.codacy.com/repositories-configure/configuring-code-patterns/) by users with the [necessary permissions](https://docs.codacy.com/organizations/roles-and-permissions-for-organizations/).

### Which tools can be configured and which name should I use?

You can use the Codacy configuration file to configure all tools supported by Codacy except the [client-side tools](https://docs.codacy.com/repositories-configure/local-analysis/client-side-tools/).

The following are the tool names that must be used in the Codacy configuration file:

```js
ameba
bandit
biome
brakeman
checkov
checkstyle
codacy-scalameta-pro
codenarc
coffeelint
cppcheck
credo
dartanalyzer
detekt
eslint-8
eslint-9
flawfinder
hadolint
jacksonlinter
lizard
markdownlint
phpcs
phpcsfixer
phpmd
pmd
pmd-7
prospector
psscriptanalyzer
pylintpython3
remark-lint
revive
roslyn
rubocop
ruff
scalastyle
opengrep
shellcheck
sonarcsharp
sonarvb
spectral
SQLint
stylelint
swiftlint
trivy
tsqllint
```

The following names are **deprecated** and shouldn't be used, although they're still accepted in the Codacy configuration file:

- `bundleraudit` - The tool **bundler-audit** [is deprecated](https://docs.codacy.com/release-notes/cloud/cloud-2023-10-13-bundler-audit-deprecation/). If you are using **Opengrep** or **Trivy** instead, use the names `trivy` or `opengrep`.
- `csslint` - The tool **CSSLint** [is deprecated](https://docs.codacy.com/release-notes/cloud/cloud-2023-10-25-csslint-jshint-fauxpas-tailor-tslint-deprecation/). If you are using **Stylelint** instead, use the name `stylelint`.
- `eslint` - Use the name `eslint-8` for **ESLint**.
- `jshint`, `tslint` - The tools **JSHint** and **TSLint** [are deprecated](https://docs.codacy.com/release-notes/cloud/cloud-2023-10-25-csslint-jshint-fauxpas-tailor-tslint-deprecation/). If you are using **ESLint** instead, use the name `eslint-8`.
- `pylint` - Use the name `pylintpython3` for **Pylint**.
- `tailor` - The tool **Tailor** [is deprecated](https://docs.codacy.com/release-notes/cloud/cloud-2023-10-25-csslint-jshint-fauxpas-tailor-tslint-deprecation/). If you are using **SwiftLint** instead, use the name `swiftlint`.

### Tool-specific configurations

By default, Codacy tries to detect which language is used on each source code file, and uses a set of default options for identifying duplicate blocks of code. However, some false positives may occur.

The tools below support specifying the language or language version used in the source code files that you're analyzing, or tuning the duplication detection.

#### Cppcheck

If you're using Cppcheck to analyze C or C++ source code files, add the following configuration to your Codacy configuration file to define the programming language you're using. The supported languages are `c` and `c++`:

```js
---
engines:
  cppcheck:
    language: c++
```

#### PHP\_CodeSniffer

If you're using the [PHP Compatibility](https://github.com/PHPCompatibility/PHPCompatibility) coding standard for PHP\_CodeSniffer, add the following configuration to your Codacy configuration file to [define the PHP version](https://github.com/PHPCompatibility/PHPCompatibility#sniffing-your-code-for-compatibility-with-specific-php-versions) you're using:

```js
---
engines:
  phpcs:
    php_version: 5.5
```

#### Legacy Pylint 1.9.\*

If you're using the legacy Pylint 1.9.\* to analyze Python source code files, add the following configuration to your Codacy configuration file to define the Python language version you're using. The supported versions are `2` and `3`:

```js
---
engines:
  pylint:
    python_version: 2
```

> [!tip] Tip
> If you're using Python 3.4.\* or later as your programming language, disable the tool **Pylint (legacy)** and enable the tool **Pylint** on your repository [Code patterns page](https://docs.codacy.com/repositories-configure/configuring-code-patterns/) instead. For more information, see [What's New in Pylint 2.0](https://pylint.pycqa.org/en/latest/whatsnew/2/2.0/index.html).

#### PMD CPD (Duplication)

Codacy uses [PMD's Copy/Paste Detector (CPD)](https://docs.pmd-code.org/latest/) to identify duplicated blocks of code [on the supported languages](https://docs.codacy.com/getting-started/supported-languages-and-tools/).

By default, Codacy only reports duplicate code blocks that have the following minimum token length, depending on the language:

| Language | Default minimum token length |
| --- | --- |
| C# | 50 |
| C/C++ | 50 |
| Go | 40 |
| Java | 100 |
| JavaScript | 40 |
| Python | 50 |
| Ruby | 50 |
| SQL | 100 |
| Scala | 50 |
| Swift | 50 |

Besides this, Codacy runs PMD CPD with the following options enabled by default:

- **Skip lexical errors:** Skip files which can't be tokenized due to invalid characters instead of aborting CPD
- **Ignore literals:** Ignore number values and string contents when comparing text
- **Ignore annotations:** Ignore language annotations when comparing text
- **Ignore usings:** Ignore `using` directives in C# when comparing text

To use a different minimum token length or change any of the default options, add your settings to the Codacy configuration file based on the example template below.

> [!important] Important
> If you configure `minTokenMatch` on the Codacy configuration file, Codacy will use that value for all languages.

```js
---
engines:
  duplication:
    minTokenMatch: 20
    skipLexicalErrors: false
    ignoreLiterals: false
    ignoreIdentifiers: true
    ignoreAnnotations: false
    ignoreUsings: false
```

## Configuring languages using a Codacy configuration file

You can use a Codacy configuration file to manage the languages that Codacy analyzes in your repository.

> [!note] Note
> Codacy applies the language settings from the Codacy configuration file as well as any settings defined [in the Codacy UI](https://docs.codacy.com/repositories-configure/languages/).

### Adding custom file extensions

To [add custom file extensions to languages](https://docs.codacy.com/repositories-configure/languages/#configuring-file-extensions) using a Codacy configuration file, you must define one or more extensions under `languages.<LANGUAGE>.extensions`. Keep in mind that some tools might not work out of the box with those extensions.

For example:

```js
---
languages:
  css:
    extensions:
      - ".scss"
```

### Disabling analysis of a language

To [disable the analysis of a specific language](https://docs.codacy.com/repositories-configure/languages/#disable-language) using a Codacy configuration file, set `languages.<LANGUAGE>.enabled` to `false`. The analysis is enabled by default for all languages.

For example:

```js
---
languages:
  css:
    enabled: false
```