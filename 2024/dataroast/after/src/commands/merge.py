from src.commands.validations import value_exists_in_dataframes, cols_exists_in_dataframe
from src.controller.events import raise_event
from src.commands.command_base import CommandArgs,Command

import pandas as pd
from pydantic.dataclasses import dataclass
from pydantic import field_validator, model_validator
from dataclasses import field
from inspect import signature

@dataclass
class MergeCommandArgs(CommandArgs):

    file1: str
    file2: str
    left_on: str
    right_on: str
    alias: str
    cols: list[str] | str = field(default_factory=list)

    
    @field_validator('cols')
    def validate_cols(cls, value):
        print(value)
        if not isinstance(value,list):
            value = value.split(',')
        print(value)
        return value

    @model_validator(mode='after')
    def validate_file_exists(self):
        if not value_exists_in_dataframes(self.model,self.file1):
            raise Exception(f"{self.file1} not present in Dataframes collection")
        if not value_exists_in_dataframes(self.model,self.file2):
            raise Exception(f"{self.file2} not present in Dataframes collection")
        return self

    @model_validator(mode='after')
    def validate_cols_exist(self):
        if not cols_exists_in_dataframe(self.model,self.file1, self.left_on):
            raise Exception(f"{self.file1} does not have column {self.left_on}")
        for col in [self.right_on,*self.cols]:
            if not cols_exists_in_dataframe(self.model,self.file2,col):
                raise Exception(f"{self.file2} does not have column {col}")
        return self

    @model_validator(mode='after')
    def set_cols(self):
        if len(self.cols) > 0:
            self.cols.append(self.right_on)
        else:
            self.cols = self.model.read(self.file2).columns.values.tolist()
        return self

class MergeCommand(Command):

    def execute(self,args: MergeCommandArgs): #type: ignore
        file1, file2, left_on, right_on, alias,cols = args.file1, args.file2, args.left_on, args.right_on, args.alias,args.cols

        suffixes = (None, '_duplicate')

        file = pd.merge(args.model.read(file1), args.model.read(file2)[cols], how='left',
                        left_on=left_on, right_on=right_on, suffixes=suffixes)

        drop_cols = [col for col in file.columns if col.endswith("_duplicate")]
        file.drop(columns=drop_cols, inplace=True)
        raise_event('merge',file)
        args.model.create(alias,file)

