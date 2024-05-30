# files=$(find . -name '*.tex')
# exclude 0_template and 1_candidatura from files
#
files=$(find . -name '*.tex' | 
    grep -v '0_template' |
    grep -v '1_candidatura')

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
echo "$glossary" > personal.txt
cat wordlist.txt >> personal.txt
sort -u personal.txt -o personal.txt

status_code=0
for file in $files; do
    misspelled=$(aspell pipe -t --lang=it_IT < "$file" |
        grep '[a-zA-Z]\+ [0-9]\+ [0-9]\+' -oh |
        grep '[a-zA-Z]\+' -o |
        aspell pipe -t --lang=en_US  |
        grep '[a-zA-Z]\+ [0-9]\+ [0-9]\+' -oh |
        grep '[a-zA-Z]\+' -o | grep -v -i -F -f  personal.txt)

    if [ -n "$misspelled" ]; then
        echo "Misspelled words in $file"
        echo "$misspelled"
        status_code=1
    fi
done

if [ "$status_code" -eq 0 ]; then
    echo "No misspelled words found."
    exit 0
fi

exit "$status_code"
