from llama.program.builder import Builder
import time


class Generator:
    """Build a dataset from seed data and augment it with new data."""

    def __init__(self, seed_dataset):
        self.seed_dataset = seed_dataset
        self.is_paired_dataset = isinstance(seed_dataset[0], list)
        self.augmented_dataset = []
        self.question_llm = Builder(id="lamini-generator", model_name="lamini/open")
        self.answer_llm = Builder(id="lamini-generator", model_name="lamini/instruct")
        self.counter = 0

    def generate(self, num_augmentations):
        """Generate a new dataset by augmenting the seed dataset."""
        questions = []
        for _ in range(num_augmentations):
            question = self._augment_questions()
            if self.is_paired_dataset:
                questions.append(question)
            else:
                self.augmented_dataset.append(question)
        if self.is_paired_dataset:
            for question in questions:
                answer = self._generate_answer(question)
                self.augmented_dataset.append([question, answer])
        return self.augmented_dataset

    def _augment_questions(self):
        """Augment the seed dataset with new data."""
        datum = self.seed_dataset[self.counter % len(self.seed_dataset)]
        d = self.question_llm(datum[0], type(datum[0]))
        self.counter += 1
        return d

    def _generate_answer(self, question):
        """Augment the seed dataset with new data."""
        datum = self.seed_dataset[self.counter % len(self.seed_dataset)]
        d = self.answer_llm(question, type(datum[1]))
        return d
