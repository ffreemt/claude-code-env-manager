# Claude Code Environment Manager - Project Documentation Index

## 📚 Documentation Overview

This documentation provides comprehensive coverage of the Claude Code Environment Manager project, including API references, architecture guides, and development guidelines.

### 🗂️ Documentation Structure

#### 📖 User Documentation
- **[README.md](README.md)** - Project overview, installation, and quick start guide
- **[User Guide](docs/USER_GUIDE.md)** - Detailed user manual with examples and workflows
- **[Configuration Guide](docs/CONFIGURATION_GUIDE.md)** - Advanced configuration options and customization
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

#### 🔧 Developer Documentation
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation with examples
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design and architectural patterns
- **[Development Guide](docs/DEVELOPMENT.md)** - Setup, testing, and contribution guidelines
- **[Code Style Guide](docs/CODE_STYLE.md)** - Coding standards and best practices

#### 🧪 Testing & Quality
- **[Quality Report](QUALITY_TEST_REPORT.md)** - Test coverage and quality metrics
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Testing strategies and framework usage
- **[Test Coverage](htmlcov/index.html)** - Interactive coverage report

#### 🏗️ Project Structure
- **[Module Index](docs/MODULE_INDEX.md)** - Cross-referenced module documentation
- **[Data Models](docs/DATA_MODELS.md)** - Data structures and validation rules
- **[CLI Reference](docs/CLI_REFERENCE.md)** - Command-line interface documentation

---

## 🎯 Quick Navigation

### For Users
1. **[Getting Started](README.md#quick-start)** - Install and run your first profile
2. **[Available Commands](README.md#commands)** - Explore all CLI commands
3. **[Configuration Examples](README.md#configuration)** - Understand config file format
4. **[Common Workflows](docs/USER_GUIDE.md#common-workflows)** - Learn typical usage patterns

### For Developers
1. **[Project Setup](docs/DEVELOPMENT.md#setup)** - Prepare development environment
2. **[API Overview](docs/API_REFERENCE.md#overview)** - Understand the core API
3. **[Architecture Patterns](docs/ARCHITECTURE.md#patterns)** - Learn system design
4. **[Testing Guidelines](docs/TESTING_GUIDE.md)** - Write effective tests

### For Contributors
1. **[Contribution Guide](docs/DEVELOPMENT.md#contributing)** - Understand contribution process
2. **[Code Standards](docs/CODE_STYLE.md)** - Follow coding conventions
3. **[Quality Requirements](QUALITY_TEST_REPORT.md)** - Meet quality benchmarks
4. **[Release Process](docs/DEVELOPMENT.md#release-process)** - Prepare releases

---

## 📊 Project Health Dashboard

| Category | Status | Metrics | Last Updated |
|----------|--------|---------|--------------|
| **Testing** | 🟡 Needs Improvement | 65/65 tests passing (31% coverage) | 2025-08-30 |
| **Code Quality** | 🔴 Critical Issues | 200+ linting violations, 25+ type errors | 2025-08-30 |
| **Documentation** | 🟢 Good | Comprehensive coverage | 2025-08-30 |
| **Dependencies** | 🟢 Stable | Up-to-date with security patches | 2025-08-30 |
| **Build Status** | 🟢 Passing | All builds successful | 2025-08-30 |

### Quality Indicators
- **Test Coverage**: 31% (Target: 80%)
- **Type Safety**: 25+ mypy errors (Target: 0)
- **Code Style**: 200+ flake8 violations (Target: 0)
- **Documentation**: 95% complete (Target: 100%)

---

## 🔗 Key Components

### Core Modules
- **[api.py](src/claude_env_manager/api.py)** - Main ClaudeEnvManager API class
- **[models.py](src/claude_env_manager/models.py)** - Data models and validation
- **[exceptions.py](src/claude_env_manager/exceptions.py)** - Custom exception classes
- **[main.py](src/claude_env_manager/main.py)** - CLI entry point

### CLI Components
- **[commands.py](src/claude_env_manager/cli/commands.py)** - CLI command implementations
- **[interface.py](src/claude_env_manager/cli/interface.py)** - TUI interface components
- **[rich_cli.py](src/claude_env_manager/rich_cli.py)** - Rich CLI utilities

### Utilities
- **[config.py](src/claude_env_manager/utils/config.py)** - Configuration management
- **[validation.py](src/claude_env_manager/utils/validation.py)** - Input validation
- **[io.py](src/claude_env_manager/utils/io.py)** - File I/O operations

---

## 🚀 Getting Started

### Installation
```bash
# Clone and install
git clone <repository-url>
cd claude-code-env-manager
pip install -e .

# Or install dependencies
pip install -r requirements.txt
```

### Basic Usage
```bash
# Initialize configuration
claude-env-manager init

# Create a profile interactively
claude-env-manager create --interactive

# List all profiles
claude-env-manager list

# Apply a profile
claude-env-manager apply development
```

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

---

## 📞 Support & Community

### Getting Help
- **Documentation**: Start with the [User Guide](docs/USER_GUIDE.md)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/claude-code/claude-code-env-manager/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/claude-code/claude-code-env-manager/discussions)

### Contributing
1. Read the [Development Guide](docs/DEVELOPMENT.md)
2. Check [open issues](https://github.com/claude-code/claude-code-env-manager/issues)
3. Fork the repository and create a feature branch
4. Follow [code standards](docs/CODE_STYLE.md) and add tests
5. Submit a pull request

---

## 📄 License & Legal

- **License**: MIT License (see [LICENSE](LICENSE))
- **Code of Conduct**: [Community Guidelines](docs/CODE_OF_CONDUCT.md)
- **Security**: [Security Policy](docs/SECURITY.md)
- **Changelog**: [Release Notes](CHANGELOG.md)

---

## 🔄 Documentation Updates

This documentation is automatically generated and maintained. For manual updates:

1. Edit the source files in the `docs/` directory
2. Run documentation generation: `python scripts/generate_docs.py`
3. Validate links: `python scripts/validate_docs.py`
4. Submit changes for review

*Last generated: 2025-08-30*