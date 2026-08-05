#!/bin/bash
# IDAHO-VAULT Dependency Installation Script
# Historical helper for ad hoc dependency repair.
# This script installs core dependencies for IDAHO-VAULT
# It is not the canonical truth surface for whether the bootstrap shard is healthy.
# Start with `python scripts/validate_bootstrap.py` and `uv.lock`.
# Note: lancedb platform compatibility issue with macOS 12 is documented as
# historical platform-specific reference material in DEPENDENCY_RESOLUTION_PLAN.md.

set -e

echo "=========================================="
echo "IDAHO-VAULT Dependency Installation"
echo "=========================================="
echo ""
echo "Historical helper only: validate the checkout first with:"
echo "  python scripts/validate_bootstrap.py"
echo "Compiled pip compatibility surface: requirements.txt"
echo ""

# Set environment variables for simdutf
if [ -d "$HOME/.local/simdutf-v5/lib" ]; then
    export LD_LIBRARY_PATH="$HOME/.local/simdutf-v5/lib:$LD_LIBRARY_PATH"
    export DYLD_LIBRARY_PATH="$HOME/.local/simdutf-v5/lib:$DYLD_LIBRARY_PATH"
    export PKG_CONFIG_PATH="$HOME/.local/simdutf-v5/lib/pkgconfig:$PKG_CONFIG_PATH"
    echo "✅ simdutf environment configured"
else
    echo "⚠️  simdutf not found at $HOME/.local/simdutf-v5/lib"
    echo "   Run: brew install simdutf (if macOS version supported)"
    echo "   Or: Build from source (see DEPENDENCY_INSTALLATION_STATUS.md)"
fi

echo ""
echo "=========================================="
echo "Installing Core Dependencies"
echo "=========================================="
echo ""

# Install pydantic (core dependency)
echo "📦 Installing pydantic..."
uv pip install --system pydantic==2.11.10

# Install json-repair (used by crewai)
echo "📦 Installing json-repair..."
uv pip install --system json-repair==0.25.3

# Install rich (for console output)
echo "📦 Installing rich..."
uv pip install --system rich==14.3.4

# Install appdirs (for file storage)
echo "📦 Installing appdirs..."
uv pip install --system appdirs==1.4.4

# Install click (CLI utilities)
echo "📦 Installing click..."
uv pip install --system click==8.1.8

# Install packaging (package utilities)
echo "📦 Installing packaging..."
uv pip install --system packaging==26.2

# Install pydantic-settings (configuration)
echo "📦 Installing pydantic-settings..."
uv pip install --system pydantic-settings==2.10.1

# Install jsonref (JSON reference handling)
echo "📦 Installing jsonref..."
uv pip install --system jsonref==1.1.0

# Install portalocker (file locking)
echo "📦 Installing portalocker..."
uv pip install --system portalocker==2.7.0

# Install python-dotenv (environment variables)
echo "📦 Installing python-dotenv..."
uv pip install --system python-dotenv==1.2.2

echo ""
echo "=========================================="
echo "Installing crewai"
echo "=========================================="
echo ""

# Install crewai without dependencies first (to avoid lancedb issue)
echo "📦 Installing crewai without dependencies..."
uv pip install --system crewai==1.14.3 --no-deps

echo ""
echo "=========================================="
echo "Installation Summary"
echo "=========================================="
echo ""

echo "✅ Core dependencies installed:"
echo "   - pydantic==2.11.10"
echo "   - json-repair==0.25.3"
echo "   - rich==14.3.4"
echo "   - appdirs==1.4.4"
echo "   - click==8.1.8"
echo "   - packaging==26.2"
echo "   - pydantic-settings==2.10.1"
echo "   - jsonref==1.1.0"
echo "   - portalocker==2.7.0"
echo "   - python-dotenv==1.2.2"
echo "   - crewai==1.14.3 (without dependencies)"
echo ""

echo "⚠️  IMPORTANT: crewai cannot be fully imported yet due to missing"
echo "    transitive dependencies caused by lancedb==0.30.0 platform"
echo "    incompatibility with macOS 12."
echo ""

echo "📋 Next Steps:"
echo "   1. Run python scripts/validate_bootstrap.py"
echo "   2. Review DEPENDENCY_RESOLUTION_PLAN.md for platform-specific history"
echo "   3. Address any remaining blockers the validator reports"
echo ""

echo "=========================================="
echo "✅ Installation script completed"
echo "=========================================="
