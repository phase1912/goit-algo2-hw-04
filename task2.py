from trie import Trie

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        """
        Count the number of words that end with the given pattern (suffix).

        Args:
            pattern: The suffix pattern to search for (must be a string)

        Returns:
            int: The number of words ending with the pattern

        Raises:
            TypeError: If pattern is not a string
            ValueError: If pattern is empty
        """
        # Validate input
        if not isinstance(pattern, str):
            raise TypeError("Pattern must be a string")

        if not pattern:
            raise ValueError("Pattern cannot be empty")

        # Get all words from the Trie using the keys() method
        all_words = self.keys()

        # Count words that end with the pattern (case-sensitive)
        count = 0
        for word in all_words:
            if word.endswith(pattern):
                count += 1

        return count

    def has_prefix(self, prefix) -> bool:
        """
        Check if there is at least one word with the given prefix.

        Args:
            prefix: The prefix to search for (must be a string)

        Returns:
            bool: True if at least one word has the prefix, False otherwise

        Raises:
            TypeError: If prefix is not a string
            ValueError: If prefix is empty
        """
        # Validate input
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")

        if not prefix:
            raise ValueError("Prefix cannot be empty")

        # Use the existing keys_with_prefix method - if it returns any keys, prefix exists
        words_with_prefix = self.keys_with_prefix(prefix)
        return len(words_with_prefix) > 0


def task2():
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat