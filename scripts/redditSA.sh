#!/bin/sh
#SBATCH --account=redditsa
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=12:00:00 
#SBATCH --mem=5G
#SBATCH --output=/project/redditsa/reddit-scraping/sentiment-results/output
#SBATCH --error=/project/redditsa/reddit-scraping/sentiment-results/error

module load miniconda3/4.12.0
conda activate /project/redditsa/redditSAModule/

python /project/redditsa/reddit-scraping/scripts/sentimentAnalyzer.py
