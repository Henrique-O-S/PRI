# Makefile

# Run ``make`` to execute pipeline
# Run ``make clean`` to delete data files

###
# Variables section
###

# List of programmes to parse for courses
programs := leic meic

# Data destination folder
path := data

# URLs and programme codes to get data from
YEAR := 2021
BASE_URL := "https://sigarra.up.pt/feup/pt/cur_geral.cur_planos_estudos_view?pv_ano_lectivo=$(YEAR)&pv_plano_id="
leic_URL := $(BASE_URL)31224
meic_URL := $(BASE_URL)31204


###
# Rules section
###

# Need to inform what to keep, otherwise these output files would be deleted
.PRECIOUS: $(addprefix $(path)/, %.courses.tsv %.html)

# Starting target rule 'all'
# Processes all programmes defined
all: $(programs)
	echo "Processed all programmes: $(programs)"

# Rule to parse programmes
# Uses 'static-pattern rules' to math the course handle
$(programs): % : %_courses
	echo "Done parsing programme $*:\n$($*_courses)\n"
	$(MAKE) $($*_courses)


# To-DO: Rule to parse each individual course
course_%:
	echo "=>Processing course with id $*"


# Rule to parse each programme's courses
# Requires a .tsv file for each programme
# Creates a variable %_courses with a list of course ids separated with spaces
%_courses: $(path)/%.courses.tsv
# sed to add a 'course_' prefix to each line
# xargs at the end to trim all whitespaces
	$(eval $@ := $(shell cat $< | cut -f1 | sed -e "s/.*/course_&/" | tr "\n" " " | xargs))
	echo "Prepared course list for $@: $($@)"

# Rule to prepare .tsv file with all courses found for a programme
# Requires a programme's HTML file to parse
$(path)/%.courses.tsv: $(path)/%.html
	cat $< | ./parse-program-html.sh > $@
	echo "Parsed HTML file to TSV at $@"

# Rule to obtain the HTML file for a programme from the web (need to convert from ISO to UTF-8)
# Requires the destination folder to be created (data)
$(path)/%.html: $(path)
	curl -s -Lo $(path)/$*.iso.html $($*_URL)
	iconv -f ISO-8859-1 -t UTF-8 $(path)/$*.iso.html > $@
	rm $(path)/$*.iso.html
	echo "Downloaded $* HTML file"

# Create data folder.
$(path):
	mkdir $(path)
	echo "Created '$(path)' folder"

# Clean all, remove all folders.
clean:
	rm -Rf $(path)
	echo "Deleted '$(path)' folder"

# EOF
