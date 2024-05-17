files=$(find . -name '*.tex')
output_file="misspelled_words.txt"
> "$output_file"  # Clear the output file if it exists
glossary=$(
    awk '/\\newglossaryentry\{[^}]*\}|acronym=\{[^}]*\}/ {
        match($0, /\\newglossaryentry\{([^}]*)\}|acronym=\{([^}]*)\}/, arr);
        if (arr[1] != "") print arr[1];
        else if (arr[2] != "") print arr[2];
    }' 2_RTB/documentazione_interna/glossario/glossario.tex
)

> personal.txt
# echo glossary to a tmp file
echo "$glossary" > personal.txt
# concat .wordlist to personal.txt
cat wordlist.txt >> personal.txt
sort -u personal.txt -o personal.txt

for file in $files; do
    misspelled=$(aspell pipe -t --lang=it_IT < "$file" |
        grep '[a-zA-Z]\+ [0-9]\+ [0-9]\+' -oh |
        grep '[a-zA-Z]\+' -o |
        aspell pipe -t --lang=en_US  |
        grep '[a-zA-Z]\+ [0-9]\+ [0-9]\+' -oh |
        grep '[a-zA-Z]\+' -o )
    # remove glossary words from misspelled words
    misspelled=$(echo "$misspelled" | grep -v -f personal.txt)
    if [ -n "$misspelled" ]; then
        echo "Misspelled words found in $file"
        echo "$misspelled" >> "$output_file"
    fi
done
sort -u "$output_file" -o "$output_file"

if [ -s "$output_file" ]; then
    echo "Misspelled words found:"
    # sort unique output file and print it
    sort -u "$output_file"
    exit 1
else
    echo "No misspelled words found."
fi
