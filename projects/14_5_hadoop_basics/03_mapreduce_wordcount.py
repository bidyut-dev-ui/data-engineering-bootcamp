#!/usr/bin/env python3
"""
Week 14.5 - Hadoop Basics: MapReduce with MRJob Tutorial
========================================================

This tutorial covers MapReduce programming using the MRJob library.
We'll implement the classic WordCount example and learn how to run
MapReduce jobs on Hadoop with 8GB RAM constraints.

Learning Objectives:
1. Understand MapReduce programming model (Map, Shuffle, Reduce)
2. Implement MapReduce jobs using MRJob Python library
3. Run jobs locally and on Hadoop cluster
4. Optimize for memory constraints and large datasets
5. Analyze job performance and debugging

Prerequisites:
- Hadoop cluster running (from 01_hadoop_docker_setup.py)
- `mrjob` Python library installed (in requirements.txt)
- Basic understanding of HDFS (from 02_hdfs_basics.py)
"""

import os
import random
import string
from collections import Counter
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol, JSONValueProtocol

class MRWordCount(MRJob):
    """
    Classic WordCount MapReduce job using MRJob.
    
    This demonstrates the basic MapReduce pattern:
    1. Mapper: emits (word, 1) for each word
    2. Combiner: sums counts locally (optional optimization)
    3. Reducer: sums counts globally
    """
    
    def mapper(self, _, line):
        """
        Mapper function: splits line into words and emits (word, 1).
        
        Args:
            _: key (ignored for text input)
            line: value (a line of text)
        
        Yields:
            (word, 1) for each word in the line
        """
        # Simple word splitting - in production you'd want better tokenization
        for word in line.strip().split():
            # Remove punctuation and convert to lowercase
            cleaned_word = word.strip(string.punctuation).lower()
            if cleaned_word:  # Skip empty strings
                yield cleaned_word, 1
    
    def combiner(self, word, counts):
        """
        Combiner function: sums counts locally before sending to reducer.
        
        This reduces network traffic by performing local aggregation.
        
        Args:
            word: key (the word)
            counts: iterator of counts (all 1s)
        
        Yields:
            (word, local_sum)
        """
        yield word, sum(counts)
    
    def reducer(self, word, counts):
        """
        Reducer function: sums all counts for each word.
        
        Args:
            word: key (the word)
            counts: iterator of counts (could be from mapper or combiner)
        
        Yields:
            (word, total_count)
        """
        yield word, sum(counts)

class MRWordCountWithStopWords(MRWordCount):
    """
    Enhanced WordCount that filters stop words and provides statistics.
    
    Demonstrates multi-step MapReduce and custom configuration.
    """
    
    # Common stop words to filter out
    STOP_WORDS = {
        'the', 'and', 'of', 'to', 'a', 'in', 'is', 'it', 'you', 'that',
        'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 'they',
        'i', 'at', 'be', 'this', 'have', 'from', 'or', 'one', 'had',
        'by', 'word', 'but', 'not', 'what', 'all', 'were', 'we', 'when',
        'your', 'can', 'said', 'there', 'use', 'an', 'each', 'which',
        'she', 'do', 'how', 'their', 'if', 'will', 'up', 'other',
        'about', 'out', 'many', 'then', 'them', 'these', 'so', 'some',
        'her', 'would', 'make', 'like', 'him', 'into', 'time', 'has',
        'look', 'two', 'more', 'write', 'go', 'see', 'number', 'no',
        'way', 'could', 'people', 'my', 'than', 'first', 'water', 'been',
        'call', 'who', 'oil', 'its', 'now', 'find', 'long', 'down',
        'day', 'did', 'get', 'come', 'made', 'may', 'part'
    }
    
    def mapper(self, _, line):
        """
        Mapper that filters stop words.
        """
        for word in line.strip().split():
            cleaned_word = word.strip(string.punctuation).lower()
            if cleaned_word and cleaned_word not in self.STOP_WORDS:
                yield cleaned_word, 1
    
    def reducer(self, word, counts):
        """
        Reducer that also categorizes words by length.
        """
        total = sum(counts)
        # Categorize word length
        length_category = 'short' if len(word) < 5 else 'medium' if len(word) < 8 else 'long'
        yield word, (total, length_category)

class MRAverageWordLength(MRJob):
    """
    MapReduce job to calculate average word length.
    
    Demonstrates more complex MapReduce pattern with multiple values.
    """
    
    def mapper(self, _, line):
        """
        Mapper emits (1, (word_length, 1)) for each word.
        Using same key to aggregate all words.
        """
        for word in line.strip().split():
            cleaned_word = word.strip(string.punctuation)
            if cleaned_word:
                yield 1, (len(cleaned_word), 1)
    
    def combiner(self, key, values):
        """
        Combiner sums lengths and counts locally.
        """
        total_length = 0
        total_count = 0
        for length, count in values:
            total_length += length
            total_count += count
        yield key, (total_length, total_count)
    
    def reducer(self, key, values):
        """
        Reducer calculates final average.
        """
        total_length = 0
        total_count = 0
        for length, count in values:
            total_length += length
            total_count += count
        
        if total_count > 0:
            average = total_length / total_count
            yield "average_word_length", f"{average:.2f}"

def generate_sample_text_file(filename, num_lines=1000, words_per_line=20):
    """
    Generate a sample text file for MapReduce processing.
    
    Args:
        filename: Output file name
        num_lines: Number of lines to generate
        words_per_line: Words per line
    """
    print(f"📝 Generating sample text file: {filename}")
    
    # Common words for more realistic distribution
    common_words = [
        'data', 'engineering', 'hadoop', 'mapreduce', 'python', 'spark',
        'database', 'query', 'analysis', 'processing', 'cluster', 'node',
        'memory', 'storage', 'file', 'system', 'distributed', 'computing',
        'algorithm', 'optimization', 'performance', 'scalability', 'reliability'
    ]
    
    all_words = common_words + [f'word_{i}' for i in range(100)]
    
    with open(filename, 'w') as f:
        for _ in range(num_lines):
            line_words = [random.choice(all_words) for _ in range(words_per_line)]
            f.write(' '.join(line_words) + '\n')
    
    file_size = os.path.getsize(filename)
    print(f"   Generated {num_lines} lines, {file_size / 1024:.1f} KB")

def run_mapreduce_locally(input_file, job_class):
    """
    Run MapReduce job locally (without Hadoop).
    
    Args:
        input_file: Input text file
        job_class: MRJob class to run
    """
    print(f"\n🔧 Running {job_class.__name__} locally:")
    
    # Create job instance
    job = job_class(args=[input_file])
    
    # Run job
    with job.make_runner() as runner:
        runner.run()
        
        # Collect results
        results = []
        for key, value in job.parse_output(runner.cat_output()):
            results.append((key, value))
        
        print(f"   Processed {input_file}")
        print(f"   Generated {len(results)} results")
        
        # Show top 10 results for WordCount
        if job_class.__name__ == 'MRWordCount' or job_class.__name__ == 'MRWordCountWithStopWords':
            results.sort(key=lambda x: x[1] if isinstance(x[1], int) else x[1][0], reverse=True)
            print("\n   Top 10 most frequent words:")
            for i, (word, count) in enumerate(results[:10]):
                if isinstance(count, tuple):
                    count_str = f"{count[0]} ({count[1]})"
                else:
                    count_str = str(count)
                print(f"      {i+1}. {word}: {count_str}")
        
        return results

def demonstrate_mapreduce_concepts():
    """
    Explain MapReduce concepts with visual examples.
    """
    print("\n" + "=" * 70)
    print("MapReduce Concepts for 8GB RAM Constraints")
    print("=" * 70)
    
    print("\n1. Map Phase:")
    print("   - Each mapper processes a split of input data")
    print("   - For 8GB RAM: split size should be 64-128MB")
    print("   - Mappers run in parallel across cluster nodes")
    print("   - Output: (key, value) pairs")
    
    print("\n2. Shuffle & Sort Phase:")
    print("   - Hadoop groups values by key")
    print("   - All values for same key go to same reducer")
    print("   - This is the most network-intensive phase")
    
    print("\n3. Reduce Phase:")
    print("   - Each reducer processes one key group")
    print("   - Aggregates values to produce final result")
    print("   - For 8GB RAM: limit reducer memory with -D mapreduce.reduce.memory.mb=1024")
    
    print("\n4. Optimization Techniques:")
    print("   - Use Combiners to reduce network traffic")
    print("   - Compress intermediate data")
    print("   - Tune number of mappers/reducers based on data size")
    print("   - Use appropriate data types (Text vs. IntWritable)")

def main():
    """
    Main tutorial function demonstrating MapReduce with MRJob.
    """
    print("=" * 70)
    print("MapReduce with MRJob Tutorial")
    print("=" * 70)
    
    # Generate sample data
    sample_file = "sample_text_data.txt"
    generate_sample_text_file(sample_file, num_lines=500, words_per_line=15)
    
    # Run basic WordCount locally
    print("\n1. Running Classic WordCount (Local Mode):")
    results_wc = run_mapreduce_locally(sample_file, MRWordCount)
    
    # Run WordCount with stop words filtering
    print("\n2. Running WordCount with Stop Words Filtering:")
    results_wc_stop = run_mapreduce_locally(sample_file, MRWordCountWithStopWords)
    
    # Run Average Word Length calculation
    print("\n3. Running Average Word Length Calculation:")
    results_avg = run_mapreduce_locally(sample_file, MRAverageWordLength)
    for key, value in results_avg:
        print(f"   {key}: {value}")
    
    # Demonstrate MapReduce concepts
    demonstrate_mapreduce_concepts()
    
    # Show how to run on Hadoop cluster
    print("\n" + "=" * 70)
    print("Running on Hadoop Cluster")
    print("=" * 70)
    
    print("\nTo run on Hadoop cluster (after HDFS setup):")
    print("1. Upload input file to HDFS:")
    print("   hdfs dfs -put sample_text_data.txt /input/")
    print("\n2. Run MRJob with Hadoop runner:")
    print("   python 03_mapreduce_wordcount.py -r hadoop sample_text_data.txt")
    print("\n3. Monitor job in ResourceManager UI:")
    print("   http://localhost:8088")
    print("\n4. Get results from HDFS:")
    print("   hdfs dfs -cat /output/part-*")
    
    # Cleanup
    print(f"\n5. Cleaning Up:")
    if os.path.exists(sample_file):
        os.remove(sample_file)
        print(f"   Removed {sample_file}")
    
    print("\n" + "=" * 70)
    print("✅ MapReduce Tutorial Completed Successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. MapReduce divides processing into Map, Shuffle, Reduce phases")
    print("2. MRJob makes Hadoop programming accessible from Python")
    print("3. Combiners reduce network traffic for better performance")
    print("4. For 8GB RAM: use appropriate split sizes and memory settings")
    print("5. Always test locally before running on cluster")

if __name__ == "__main__":
    # Note: When running with MRJob, use command line:
    # python 03_mapreduce_wordcount.py input.txt
    # For this tutorial, we run the main() function directly
    main()