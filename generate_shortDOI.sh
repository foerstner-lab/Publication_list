for DOI in $(cut -f 1 Publications.tsv | grep -v DOI)
do
    SHORT_DOI=$(curl -s "http://shortdoi.org/${DOI}"  | grep "http://doi.org/" | sed -e "s/.*doi.org\///" -e "s/<.*//" 2> /dev/null)
    printf "${DOI}\t${SHORT_DOI}\n"
done
