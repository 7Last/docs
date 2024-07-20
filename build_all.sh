# find all files variables.tex
files=(
  "./3_PB/documentazione_esterna/analisi_dei_requisiti/analisi_dei_requisiti.tex"
  "./3_PB/documentazione_esterna/piano_di_progetto/piano_di_progetto.tex"
  "./3_PB/documentazione_esterna/piano_di_qualifica/piano_di_qualifica.tex"
  "./3_PB/documentazione_esterna/specifica_tecnica/specifica_tecnica.tex"
  "./3_PB/documentazione_interna/glossario/glossario.tex"
  "./3_PB/documentazione_interna/norme_di_progetto/norme_di_progetto.tex"
  "./3_PB/verbali_esterni/verbale_esterno_2024-06-05/verbale_esterno_2024-06-05.tex"
  "./3_PB/verbali_esterni/verbale_esterno_2024-06-12/verbale_esterno_2024-06-12.tex"
  "./3_PB/verbali_esterni/verbale_esterno_2024-06-19/verbale_esterno_2024-06-19.tex"
  "./3_PB/verbali_esterni/verbale_esterno_2024-06-26/verbale_esterno_2024-06-26.tex"
  "./3_PB/verbali_esterni/verbale_esterno_2024-07-03/verbale_esterno_2024-07-03.tex"
  "./3_PB/verbali_interni/verbale_interno_2024-06-12/verbale_interno_2024-06-12.tex"
  "./3_PB/verbali_interni/verbale_interno_2024-06-19/verbale_interno_2024-06-19.tex"
  "./3_PB/verbali_interni/verbale_interno_2024-06-26/verbale_interno_2024-06-26.tex"
  "./3_PB/verbali_interni/verbale_interno_2024-07-03/verbale_interno_2024-07-03.tex"
  "./3_PB/verbali_interni/verbale_interno_2024-07-10/verbale_interno_2024-07-10.tex"
  "./3_PB/verbali_interni/verbale_interno_2024-07-17/verbale_interno_2024-07-17.tex"
)

for file in ${files[@]}; do
  cd $(dirname $file)
  pdflatex -interaction=batchmode $(basename $file)
  echo "File $(basename $file .tex).pdf created"
  cd -
done