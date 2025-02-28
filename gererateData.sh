for word in `cat google-10000-english.txt`
do
  echo $word
  python3 main.py --query "$word" --since 2007-01-01 --max-tweets 1000000
done