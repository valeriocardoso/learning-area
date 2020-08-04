import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator


class OtherTransformer(TransformerMixin, BaseEstimator):
    def __init__(self, columns='auto', name='Other'):
        self._columns_levels = {}
        self._rare_col = name
        self._cat_cols = columns

    def _other_transformation(self, X):
        # se o atributo columns_levels for um dicionário vazio, ou seja,
        # se o método ainda não tiver sido aplicado
        if self._columns_levels == {}:
            # checando se a identificação de colunas categóricas é automática
            if self._cat_cols == 'auto':
                # trazendo o nome de todas as colunas do tipo object
                self._cat_cols = X.select_dtypes(
                    include=['object']).columns.tolist()
                # iterando a lista de colunas object
            for col in self._cat_cols:
                # extraindo de cada coluna do loop os níveis únicos
                series_count_elements = pd.value_counts(X[col], normalize=True)
                # identificação do nível menos frequente de acordo com o threshold definido
                mask = (series_count_elements *
                        100).lt(series_count_elements.min()*100 + 0.01)
                # substituição do nível menos frequente pelo termo escolhido
                X[col] = np.where(X[col].isin(series_count_elements[mask].index),
                                  self._rare_col, X[col])
                # guardando os níveis da coluna no dicionário
                self._columns_levels[col] = X[col].value_counts(
                ).index.tolist()
            return X
        else:
            # caso o atributo self._columns_levels já esteja definido
            for col in self._cat_cols:
                for element in X[col].unique().tolist():
                    # se o nível de classe não existir no dicionário,
                    # ele atribui ao novo nível o termo escolhido
                    if element not in self._columns_levels[col]:
                        X.loc[X[col] == element, col] = self._rare_col
                    else:
                        continue
            return X

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # chamada para o método auxiliar
        X = X.copy()
        return self._other_transformation(X)

    def get_params(self, deep=True):
        # retorna um dicionário com os atributos e seus respectivos valores
        return {"columns_levels": self._columns_levels,
                "name": self._rare_col, "columns": self._cat_cols}

    def set_params(self, **parameters):
        # iterando pelos elementos passados e definindo-os na classe
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
