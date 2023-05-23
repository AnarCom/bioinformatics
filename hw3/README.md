# Homework 3
1. [Ген, взятый для анализа](https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR24502286&display=download)
2. Скрипт (action.sh) является скриптом, который выполняет все данные (запускает все инструменты), в том числе и сравнивает показатель "удачности" чтения.
3. 
```text
15644 + 0 in total (QC-passed reads + QC-failed reads)
13760 + 0 primary
1269 + 0 secondary
615 + 0 supplementary
0 + 0 duplicates
0 + 0 primary duplicates
14907 + 0 mapped (95.29% : N/A)
13023 + 0 primary mapped (94.64% : N/A)
0 + 0 paired in sequencing
0 + 0 read1
0 + 0 read2
0 + 0 properly paired (N/A : N/A)
0 + 0 with itself and mate mapped
0 + 0 singletons (N/A : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5)

```
4. Проблема состоит в том, что bash не умеет работать с float, так что было принято решение распарсить это все используя python, который вызывается из bash. (СМ скрипт из пункта 2)

5. Было принято решение не развертывать готовый образ, а взять docker с apache airflow и добавить туда инструменты для биоинформатики (почти все пакеты уже были в других операционных системах, но вот freebayes заводится из пакетного менеджера под других операционных системах отказывался). Контейнер docker так же располагается в папке.







[помогла вот такая штука](https://asciinema.org/a/316273?autoplay=1)