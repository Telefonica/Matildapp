######################################
### Types hints remover for python ###
##  You need to install:           ###
##   - pip install strip-hints     ###
##   - pip install format          ###
######################################

files="$(find . -name '*.py')"

for file in $files; do
    strip-hints "$file" -o "$file" --to-empty
    echo "Strip hints from $file"
done

# Format the code
for file in $files; do
    autopep8 --in-place --aggressive $file
    echo "Formatted $file"
done
