# Contributing to Manganova API

Thank you for considering contributing to Manganova API! We welcome contributions from everyone. Below are some guidelines to help you get started.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on our [GitHub Issues](https://github.com/your-repo/manganova.api/issues) page. Include as much detail as possible to help us understand and reproduce the issue.

### Feature Requests

We welcome new feature requests! Please create an issue on our [GitHub Issues](https://github.com/your-repo/manganova.api/issues) page and describe the feature you would like to see, why you need it, and how it should work.

### Code Contributions

1. **Fork the Repository**: Fork the repository on GitHub and clone it to your local machine.
2. **Create a Branch**: Create a new branch for your feature or bugfix.

   ```sh
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**: Make your changes in your local repository.
4. **Commit Changes**: Commit your changes with a clear and concise commit message. (Check [Commitizen](#commitizen))

   ```sh
   cz c
   ```

5. **Push Changes**: Push your changes to your forked repository.

   ```sh
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**: Create a pull request to the main repository. Provide a detailed description of your changes and any related issue numbers.

### Code Style

Please follow the coding style used in the project. Ensure your code is well-documented and includes comments where necessary.

#### Commitizen

This project uses Commitizen to standardize commit messages and generate changelogs. Please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification when making commits. You can use the following command to commit your changes:

```sh
cz commit
```

#### Ruff

We use [Ruff](https://docs.astral.sh/ruff) as our code linter and formatter to ensure code quality and consistency. Please run Ruff before pushing your changes:

```sh
ruff check . --fix
ruff format .
```

Alternatively, you can use the [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) for Visual Studio Code to automatically lint and format your code as you work.

Make sure your code passes all linting checks.

### Testing

Ensure that your changes do not break existing tests and add new tests for your changes if applicable. Run all tests to verify.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## Contact

If you have any questions or need further assistance, feel free to reach out to the maintainers.

Thank you for contributing!
