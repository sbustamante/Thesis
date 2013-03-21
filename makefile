edit_thesis_sp:
	texmaker ./thesis_spanish/dissertation_sp.tex &

edit_kate:
	kate thesis_schedule thesis_figures thesis_content  ./codes/Analysis_Codes/* &

git_update:
	git add \
	thesis_content				\
	thesis_figures				\
	thesis_schedule				\
	Readme					\
	makefile				\
	thesis_spanish/figures/* 		\
	thesis_spanish/Latex/* 			\
	thesis_spanish/chapters/*.tex 		\
	thesis_spanish/chapters/*.bib		\
	thesis_spanish/dissertation_sp.tex	\
	thesis_spanish/dissertation_sp.pdf	\
	codes/Halo_Finder/*			\
	codes/Analysis_Codes/*			\
	codes/Theoretical_Codes/*

	git commit -m 'Last changes'

	
