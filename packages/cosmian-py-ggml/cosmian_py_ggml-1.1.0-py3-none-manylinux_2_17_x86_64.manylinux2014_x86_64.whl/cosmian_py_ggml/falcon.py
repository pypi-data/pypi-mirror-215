# -*- coding: utf-8 -*-
import pathlib
import threading
import time
from ctypes import CDLL, POINTER, c_char_p, c_float, c_int32, c_void_p
from typing import Callable, List, Optional

library_path = pathlib.Path(__file__).parent.resolve() / "libggml-bindings.so"
clibrary = CDLL(str(library_path))


class FalconModel:
    """
    Falcon model bindings for GGML.
    """

    def __init__(self, model_path: str):
        """
        Load Falcon model from the given model path.

        Args:
            model_path (str): Path to the model file.
        """
        func = clibrary.falcon_load_model
        func.argtypes = [c_char_p]
        func.restype = c_void_p

        self.ggml_model = func(model_path.encode("utf-8"))

    def __del__(self):
        """
        Free the memory allocated for the model.
        """

        func = clibrary.falcon_free_model
        func.argtypes = [c_void_p]
        func.restype = c_int32

        func(self.ggml_model)

    def __call__(
        self,
        tokens: List[int],
        n_predict: int = 200,
        n_threads: int = 6,
        seed: int = -1,
        n_batch: int = 8,
        top_k: int = 40,
        top_p: float = 0.9,
        temp: float = 0.9,
        eos_token_id: int = 11,
        stream_callback: Optional[Callable[[List[int]], None]] = None,
    ) -> List[int]:
        """
        Generate tokens using the Falcon model.

        Args:
            tokens (List[int]): List of input tokens.
            n_predict (int): Number of tokens to predict. Defaults to 200.
            n_threads (int, optional): Number of threads to use for processing. Defaults to 6.
            seed (int, optional): The seed for the random number generator. Defaults to -1.
            n_batch (int, optional): Batch size for prompt processing. Defaults to 8.
            top_k (int, optional): Top-k sampling parameter. Defaults to 40.
            top_p (float, optional): Top-p sampling parameter. Defaults to 0.9.
            temp (float, optional): Temperature parameter. Defaults to 0.9.
            eos_token_id (int, optional): End of text special token id. Defaults to 11.
            stream_callback (Optional[Callable[[List[int]], None]]): Optional callback function to receive generated tokens.

        Returns:
            List[int]: List of generated tokens.
        """
        func = clibrary.falcon_generate
        func.argtypes = [
            c_void_p,  # model
            POINTER(c_int32),  # input tokens array
            c_int32,  # input tokens length
            POINTER(c_int32),  # output tokens array
            c_int32,  # n_predict
            c_int32,  # n_threads
            c_int32,  # seed
            c_int32,  # n_batch
            c_int32,  # top_k
            c_float,  # top_p
            c_float,  # temp
        ]

        # Convert input tokens to a C-compatible array
        input_tokens_len = len(tokens)
        input_tokens_arr = (c_int32 * input_tokens_len)()
        for i in range(input_tokens_len):
            input_tokens_arr[i] = tokens[i]

        # Create an array for output tokens and initialize with zeros
        # Add a last end_of_text token (0) at the end
        output_tokens_len = n_predict + 1
        output_tokens_arr = (c_int32 * (output_tokens_len))()
        for i in range(output_tokens_len):
            output_tokens_arr[i] = eos_token_id

        # Initialize thread_stop_event if stream_callback is provided
        thread_stop_event: Optional[threading.Event] = None
        if stream_callback:
            thread_stop_event = threading.Event()

            # Define a thread to handle streaming of generated tokens
            def stream_thread():
                num_printed_tokens = 0
                while True:
                    time.sleep(0.5)
                    tokens = [output_tokens_arr[i] for i in range(output_tokens_len)]
                    curr_len = tokens.index(eos_token_id)
                    if curr_len > num_printed_tokens:
                        stream_callback(tokens[num_printed_tokens:curr_len])
                        num_printed_tokens = curr_len

                    if thread_stop_event.is_set():
                        break

            # Start the stream_thread
            threading.Thread(target=stream_thread).start()

        # Start tokens generation on GGML backend
        func(
            self.ggml_model,
            input_tokens_arr,
            input_tokens_len,
            output_tokens_arr,
            n_predict,
            n_threads,
            seed,
            n_batch,
            top_k,
            top_p,
            temp,
        )

        # Stop the stream_thread if it was started
        if thread_stop_event is not None:
            time.sleep(1)
            thread_stop_event.set()

        # Retrieve the generated tokens and return them
        output_tokens = [output_tokens_arr[i] for i in range(output_tokens_len)]
        return output_tokens[: output_tokens.index(eos_token_id) + 1]
