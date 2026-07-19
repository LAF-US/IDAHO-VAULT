# MacPorts
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"

# NVM
export NVM_DIR="$HOME/.nvm"
if [ -s "/usr/local/opt/nvm/nvm.sh" ]; then
  \. "/usr/local/opt/nvm/nvm.sh"
elif [ -s "$NVM_DIR/nvm.sh" ]; then
  \. "$NVM_DIR/nvm.sh"
fi
if [ -s "/usr/local/opt/nvm/etc/bash_completion.d/nvm" ]; then
  \. "/usr/local/opt/nvm/etc/bash_completion.d/nvm"
elif [ -s "$NVM_DIR/bash_completion" ]; then
  \. "$NVM_DIR/bash_completion"
fi

# OpenCode
export PATH="$HOME/.opencode/bin:$PATH"

# Node: nvm via Homebrew, system node at /usr/local/bin, and home-dir project bins
export PATH="$HOME/node_modules/.bin:$PATH"

# Hermes Agent — ensure ~/.local/bin is on PATH
export PATH="$HOME/.local/bin:$PATH"

# Python user scripts: jupyter, jupytext, nbconvert
export PATH="$HOME/Library/Python/3.13/bin:$PATH"

# Added by Obsidian
export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"
