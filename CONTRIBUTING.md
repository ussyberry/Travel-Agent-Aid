# Contributing to Travel Agent Assistant

Thank you for your interest in contributing to Travel Agent Assistant! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

1. **Check existing issues** - Make sure the bug hasn't already been reported
2. **Create a new issue** - Use the bug report template
3. **Provide details:**
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages or screenshots if applicable

### Suggesting Features

1. **Check existing issues** - See if the feature has been suggested
2. **Create a feature request** - Use the feature request template
3. **Describe:**
   - The feature and its use case
   - How it would benefit users
   - Possible implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes:**
   - Follow the coding style (see below)
   - Add tests for new functionality
   - Update documentation as needed
4. **Commit your changes:**
   ```bash
   git commit -m "Add: description of your changes"
   ```
   Use clear, descriptive commit messages
5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request:**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure all tests pass

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Travel-Agent-Aid.git
   cd Travel-Agent-Aid
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

5. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add comments for complex logic

**Example:**
```python
def search_flights(origin, destination, departure_date, adults=1):
    """
    Searches for flights using the Amadeus API.
    
    Args:
        origin (str): IATA airport code for origin
        destination (str): IATA airport code for destination
        departure_date (str): Departure date in YYYY-MM-DD format
        adults (int): Number of adult passengers (default: 1)
    
    Returns:
        list: List of flight offers, or None if error occurs
    """
    # Implementation here
```

### JavaScript

- Use meaningful variable names
- Add comments for complex logic
- Follow consistent indentation (2 or 4 spaces)
- Handle errors gracefully

### Git Commit Messages

- Use clear, descriptive messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Add more details in the body if needed

**Good examples:**
- `Add: Error handling for API rate limits`
- `Fix: CORS issue in flight search endpoint`
- `Update: README with installation instructions`

## Testing

- Write tests for new features
- Ensure existing tests still pass
- Aim for good test coverage
- Test both success and error cases

**Example test structure:**
```python
def test_search_flights_success():
    """Test successful flight search."""
    # Arrange
    origin = "JFK"
    destination = "LHR"
    departure_date = "2025-06-15"
    
    # Act
    result = search_flights(origin, destination, departure_date)
    
    # Assert
    assert result is not None
    assert isinstance(result, list)
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update API documentation if endpoints change
- Include examples in docstrings when helpful

## Project Structure

- **Backend code** goes in `backend/`
- **Frontend code** goes in `frontend/`
- **Tests** go in `backend/tests/`
- **Documentation** files in root directory

## Areas for Contribution

We welcome contributions in these areas:

- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🧪 Test coverage
- 🎨 UI/UX improvements
- ⚡ Performance optimizations
- 🔒 Security enhancements
- 🌐 Internationalization

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues and discussions
- Review the codebase to understand patterns

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md (if we create one)
- Release notes
- Project documentation

Thank you for contributing to Travel Agent Assistant! 🎉

