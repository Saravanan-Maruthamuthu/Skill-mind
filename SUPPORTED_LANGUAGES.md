# Supported Programming Languages

This document lists all programming languages supported by the AI Interview Assistant for coding challenges.

## Language Support via Judge0 API

The system uses **Judge0 CE (Community Edition)** API for online code execution, supporting **35+ programming languages** without requiring local compiler installations.

### Mainstream Languages
- ✅ **Python 3** (3.8.1)
- ✅ **Java** (OpenJDK 13.0.1)
- ✅ **C** (GCC 9.2.0)
- ✅ **C++** (GCC 9.2.0) - includes C++14, C++17, C++20
- ✅ **C#** (Mono 6.6.0.161)
- ✅ **JavaScript** (Node.js 12.14.0)
- ✅ **TypeScript** (3.7.4)
- ✅ **PHP** (7.4.1)
- ✅ **Ruby** (2.7.0)
- ✅ **Go** (1.13.5)
- ✅ **Rust** (1.40.0)
- ✅ **Bash** (5.0.0)

### Modern Languages
- ✅ **Swift** (5.2.3)
- ✅ **Kotlin** (1.3.70)
- ✅ **Dart** (2.19.2)
- ✅ **Scala** (2.13.2)
- ✅ **Groovy** (3.0.3)

### Functional Languages
- ✅ **Haskell** (GHC 8.8.1)
- ✅ **Elixir** (1.9.1)
- ✅ **Clojure** (1.10.1)
- ✅ **F#** (.NET Core SDK 3.1.202)

### Scripting Languages
- ✅ **Lua** (5.3.5)
- ✅ **Perl** (5.28.1)
- ✅ **R** (4.0.0)

### Legacy Languages
- ✅ **COBOL** (GnuCOBOL 2.2)
- ✅ **Fortran** (GFortran 9.2.0)
- ✅ **Pascal** (FPC 3.0.4)

### System Languages
- ✅ **Assembly** (NASM 2.14.02)
- ✅ **Objective-C** (Clang 7.0.1)

### Logic & Database
- ✅ **Prolog** (GNU Prolog 1.4.5)
- ✅ **SQL** (SQLite 3.27.2)

## Language-Agnostic Challenges

Users can solve **any coding challenge in any supported language**. The language validation has been removed, allowing maximum flexibility:

- A challenge originally designed for C can be solved in Java, Python, Kotlin, etc.
- Users can select their preferred language from the dropdown
- All test cases are executed in the selected language
- No local compiler/interpreter installation required

## How It Works

1. **Frontend**: Language selector with 35+ options
2. **Backend**: Judge0Client maps language names to Judge0 API language IDs
3. **Execution**: Code is sent to Judge0 CE API for compilation and execution
4. **Results**: Test case results are returned with output comparison

## Adding More Languages

To add support for additional languages available in Judge0:

1. Add language ID to `backend/modules/judge0_client.py` in `LANGUAGE_IDS` dictionary
2. Add boilerplate code to `frontend/js/coding-challenge.js` in `boilerplates` object
3. Add language option to `languageList` array in `coding-challenge.js`

## API Endpoint

- **Judge0 CE API**: `https://ce.judge0.com`
- **Documentation**: https://ce.judge0.com
- **Public Access**: No API key required for basic usage
