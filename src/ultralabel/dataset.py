# Copyright 2023-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING, Union

from datasets import Dataset

try:
    import argilla as rg

    _argilla_installed = True
except ImportError:
    _argilla_installed = False


if TYPE_CHECKING:
    from argilla import FeedbackDataset

    from ultralabel.tasks.base import Task


class CustomDataset(Dataset):
    task: Union["Task", None] = None

    def to_argilla(self) -> "FeedbackDataset":
        if _argilla_installed is False:
            raise ImportError(
                "The argilla library is not installed. Please install it with `pip install argilla`."
            )
        if self.task is None:
            raise ValueError(
                "The task is not set. Please set it with `dataset.task = <task>`."
            )

        rg_dataset = rg.FeedbackDataset(
            fields=self.task.to_argilla_fields(dataset_row=self[0]),
            questions=self.task.to_argilla_questions(dataset_row=self[0]),
        )
        rg_dataset.add_records(
            [
                self.task.to_argilla_record(dataset_row=dataset_row)
                for dataset_row in self
            ]
        )
        return rg_dataset


class PreferenceDataset(Dataset):
    task: Union["Task", None] = None

    def to_argilla(self, group_ratings_as_ranking: bool = False) -> "FeedbackDataset":
        if _argilla_installed is False:
            raise ImportError(
                "The argilla library is not installed. Please install it with `pip install argilla`."
            )
        if self.task is None:
            raise ValueError(
                "The prompt template is not set. Please set it with `dataset.task = <task>`."
            )
        rg_dataset = rg.FeedbackDataset(
            fields=self.task.to_argilla_fields(dataset_row=self[0]),
            questions=self.task.to_argilla_questions(
                dataset_row=self[0], group_ratings_as_ranking=group_ratings_as_ranking
            ),
        )
        rg_dataset.add_records(
            [
                self.task.to_argilla_record(
                    dataset_row=dataset_row,
                    group_ratings_as_ranking=group_ratings_as_ranking,
                )
                for dataset_row in self
            ]
        )
        return rg_dataset