# Dependency Resolution Plan - IDAHO-VAULT

## 🎯 EXECUTIVE SUMMARY

### ✅ COMPLETED TASKS

1. **simdutf System Library Installation** ✅
   - Built simdutf v5.0.0 from source
   - Installed to: `~/.local/simdutf-v5/`
   - Library: `libsimdutf.6.0.0.dylib`
   - Headers and CMake config available
   - Environment variables configured

2. **Core Python Dependencies Installation** ✅
   - pydantic==2.11.10 ✅
   - json-repair==0.25.3 ✅
   - rich==14.3.4 ✅
   - appdirs==1.4.4 ✅
   - click==8.1.8 ✅
   - packaging==26.2 ✅
   - pydantic-settings==2.10.1 ✅
   - jsonref==1.1.0 ✅
   - portalocker==2.7.0 ✅
   - python-dotenv==1.2.2 ✅
   - numpy==2.4.4 ✅
   - crewai==1.14.3 ✅ (installed without dependencies)

3. **Environment Configuration** ✅
   - LD_LIBRARY_PATH configured
   - DYLD_LIBRARY_PATH configured  
   - PKG_CONFIG_PATH configured
   - simdutf library accessible

### ⚠️ BLOCKING ISSUE

**Problem**: lancedb==0.30.0 has no wheels for macOS 12.0 (current version)

**Impact**: 
- crewai==1.14.3 depends on lancedb>=0.29.2,<0.30.1
- Cannot install crewai with full dependencies
- Cannot import crewai due to missing transitive dependencies (chromadb → lancedb)

**Available lancedb Wheels**:
- manylinux_2_17_aarch64
- manylinux_2_17_x86_64
- manylinux_2_28_aarch64
- manylinux_2_28_x86_64
- macosx_11_0_arm64 ⚠️ (older macOS version)
- win_amd64

**Missing**: macosx_12_0_x86_64 (current macOS version)

---

## 📋 RESOLUTION STRATEGIES

### Strategy 1: Install lancedb from Source (RECOMMENDED) ⭐

**Steps**:
```bash
# Install build dependencies
uv pip install --system cmake ninja

# Clone lancedb repository
cd /tmp
git clone https://github.com/lancedb/lancedb.git
cd lancedb

# Build from source with custom prefix
mkdir -p build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/.local/lancedb \
          -DBUILD_SHARED_LIBS=ON \
          -DBUILD_TESTING=OFF
make -j$(sysctl -n hw.ncpu)
make install

# Add to environment
export LD_LIBRARY_PATH="$HOME/.local/lancedb/lib:$LD_LIBRARY_PATH"
```

**Pros**:
- Full functionality restored
- No platform limitations
- Future-proof

**Cons**:
- Requires more time
- Needs build tools (cmake, ninja)

---

### Strategy 2: Use Alternative Vector Database

**Options**:
1. **Use chromadb without lancedb** (if possible)
2. **Use SQLite-based memory** (crewai memory backend)
3. **Use in-memory only** (disable persistent storage)
4. **Use Milvus Lite** (lightweight vector database)
5. **Use Qdrant** (vector similarity search engine)

**Commands**:
```bash
# Option 4: Milvus Lite
uv pip install --system milvus

# Option 5: Qdrant
uv pip install --system qdrant-client
```

**Pros**:
- No platform compatibility issues
- Simpler setup
- Milvus and Qdrant are actively maintained

**Cons**:
- May lose functionality
- Different performance characteristics
- Requires code changes to use alternative DB

**Integration Notes**:
- Milvus Lite: Lightweight, single-binary deployment
- Qdrant: High-performance, supports filtering and hybrid search
- Both support Python client libraries

---

### Strategy 3: Upgrade macOS or Use Different Machine

**Options**:
1. Upgrade to macOS 13+ (Ventura or later)
2. Use a different machine with newer macOS
3. Use Linux (Ubuntu 22.04+ or similar)
4. Use Windows WSL2

**Pros**:
- Native wheel support
- No workarounds needed

**Cons**:
- Requires OS upgrade
- May not be feasible for all users

---

### Strategy 4: Use Docker Container

**Steps**:
```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
pip install uv

# Clone and install IDAHO-VAULT
WORKDIR /app
COPY . /app
RUN uv pip install --system -r requirements.txt

# Set up environment
ENV LD_LIBRARY_PATH="/usr/local/lib"

CMD ["python3", "-m", "idaho_vault.main"]
EOF

# Build and run
docker build -t idaho-vault .
docker run -it idaho-vault
```

**Pros**:
- Isolated environment
- No OS compatibility issues
- Reproducible

**Cons**:
- Requires Docker
- Slightly more complex workflow

---

## 🔧 IMMEDIATE ACTIONS (Choose One)

### Action A: Build lancedb from Source (Recommended)
```bash
cd /tmp
git clone https://github.com/lancedb/lancedb.git
cd lancedb
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/.local/lancedb -DBUILD_SHARED_LIBS=ON
make -j$(sysctl -n hw.ncpu)
make install

export LD_LIBRARY_PATH="$HOME/.local/lancedb/lib:$LD_LIBRARY_PATH"
```

### Action B: Use Docker
```bash
docker build -t idaho-vault .
docker run -it idaho-vault
```

### Action C: Manual Dependency Installation (Partial)
```bash
# Install remaining dependencies manually
uv pip install --system \
  chromadb==1.1.1 \
  lancedb==0.30.0 \
  # ... continue with other dependencies from requirements.txt
```

---

## 📊 VERIFICATION CHECKLIST

### Before Proceeding:
- [ ] simdutf installed: `ls ~/.local/simdutf-v5/lib/libsimdutf*`
- [ ] Environment variables set: `echo $LD_LIBRARY_PATH`
- [ ] Python 3.13.7 available: `python3 --version`
- [ ] uv installed: `which uv`

### After Installation:
- [ ] crewai imports: `python3 -c "import crewai; print('OK')"`
- [ ] IDAHO-VAULT imports: `python3 -c "from idaho_vault import main; print('OK')"`
- [ ] Crew can be created: `python3 -c "from idaho_vault.crew import IdahoVaultBootstrapCrew; print('OK')"`

---

## 📚 DOCUMENTATION REFERENCES

1. **simdutf**: https://github.com/simdutf/simdutf
   - Unicode conversion library
   - Successfully installed v5.0.0

2. **lancedb**: https://github.com/lancedb/lancedb
   - Vector database
   - Platform compatibility issue with macOS 12

3. **CrewAI**: https://github.com/joaomdmoura/crewAI
   - AI agent framework
   - Depends on chromadb → lancedb

4. **uv**: https://github.com/astral-sh/uv
   - Fast Python package installer
   - Used for all installations

---

## 🎓 LESSONS LEARNED

### Key Insight: System Libraries vs Python Packages

**System Libraries** (must be installed separately):
- simdutf (C++ Unicode library) ✅ DONE
- lancedb (Vector database) ⚠️ BLOCKER
- chromadb (Vector database) ⚠️ DEPENDS ON LANCEDB
- icu4c (Unicode support) - may need
- openssl (Cryptography) - usually system-wide

**Python Packages** (install via pip/uv):
- crewai ✅ INSTALLED
- pydantic ✅ INSTALLED
- json-repair ✅ INSTALLED
- rich ✅ INSTALLED
- And 400+ others ✅ PARTIALLY INSTALLED

### Best Practice for Future:
1. Check if dependency is a system library or Python package
2. Install system libraries via system package manager or from source
3. Set LD_LIBRARY_PATH, DYLD_LIBRARY_PATH, PKG_CONFIG_PATH
4. Then install Python packages

---

## 📝 NEXT STEPS

### Step 1: Choose a Resolution Strategy
Decide which strategy to use from the options above.

### Step 2: Execute the Chosen Strategy
Follow the commands for your chosen strategy.

### Step 3: Verify Installation
```bash
# Test imports
python3 -c "import crewai; print('✅ crewai works')"
python3 -c "from idaho_vault.crew import IdahoVaultBootstrapCrew; print('✅ IDAHO-VAULT works')"

# Test main entrypoint
python3 -m idaho_vault.main --help
```

### Step 4: Update Documentation
Update DEPENDENCY_INSTALLATION_STATUS.md with actual results.

---

## 🚨 TROUBLESHOOTING

### Error: "Library not found"
**Solution**: Ensure environment variables are set correctly:
```bash
export LD_LIBRARY_PATH="$HOME/.local/simdutf-v5/lib:$LD_LIBRARY_PATH"
export DYLD_LIBRARY_PATH="$HOME/.local/simdutf-v5/lib:$DYLD_LIBRARY_PATH"
export PKG_CONFIG_PATH="$HOME/.local/simdutf-v5/lib/pkgconfig:$PKG_CONFIG_PATH"
```

### Error: "No matching distribution found"
**Solution**: The package is a system library, not a Python package:
```bash
# For simdutf:
# Built from source ✅ DONE

# For lancedb:
# Build from source ⚠️ TO DO
```

### Error: Platform incompatibility
**Solution**: Build from source or upgrade OS:
```bash
# Build from source (recommended for lancedb)
cd /tmp
git clone https://github.com/lancedb/lancedb.git
cd lancedb
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/.local/lancedb
make -j$(sysctl -n hw.ncpu)
make install
```

---

## 📞 SUPPORT

- **IDAHO-VAULT Issues**: Check DEPENDENCY_INSTALLATION_STATUS.md
- **simdutf Issues**: https://github.com/simdutf/simdutf/issues
- **lancedb Issues**: https://github.com/lancedb/lancedb/issues
- **CrewAI Issues**: https://github.com/joaomdmoura/crewAI/issues

---

**Created**: 2026-04-27  
**Last Updated**: 2026-04-27  
**Status**: Resolution plan complete, awaiting execution of chosen strategy
