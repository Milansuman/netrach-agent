"""
Classes and decorators for custom evaluators in netra.
"""
from dataclasses import dataclass
import inspect
from .observability import initialize_netra
from netra import Netra, SpanType
from langchain_ollama import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import sys

embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")

@dataclass
class EvaluatorTestCase:
    """
    Test case base class for custom evaluator.
    """
    name: str

    def is_embedding_similar(self, a: str, b: str, threshold: float) -> None:
        [embedding_a, embedding_b] = embedding_model.embed_documents([a, b])
        assert cosine_similarity([embedding_a], [embedding_b])[0][0] <= threshold, f"Embeddings are not similar enough: {cosine_similarity([embedding_a], [embedding_b])[0][0]} < {threshold}"
    
    def execute(self) -> bool:
        test_funcs = inspect.getmembers(self, predicate=lambda obj: inspect.ismethod(obj) and obj.__name__.startswith("test_"))

        with Netra.start_span(f"evaluator_tests.{self.name}") as test_span:
            for test_name, test_func in test_funcs:
                with Netra.start_span(f"test_case.{test_name}", as_type=SpanType.SPAN) as case_span:
                    try:
                        test_func()
                        case_span.set_success()
                        print(f"[PASS] {self.name}.{test_name}")
                    except AssertionError as e:
                        print(f"[FAIL] {self.name}.{test_name} - {str(e)}")
                        case_span.set_error(str(e))
            

def main(module="__main__"):
    """
    Test executor class for custom evaluators.
    """
    initialize_netra()
    eval_classes = inspect.getmembers(
        sys.modules[module], 
        predicate=lambda obj: 
            inspect.isclass(obj) and issubclass(obj, EvaluatorTestCase) and obj is not EvaluatorTestCase
    )

    for _, eval_class in eval_classes:
        evaluator = eval_class()
        evaluator.execute()
