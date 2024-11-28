import codecs
import gzip
import pickle

from matplotlib import pyplot
from pandas import DataFrame

from performance_library.conformance_metric_functions import EcdfConformanceMetrics
from performance_library.ecdf import Ecdf


def deserialize_objects(value):
    step1 = codecs.decode(value.encode(), "base64")
    step2 = gzip.decompress(step1)
    step3 = pickle.loads(step2)
    return step3


class AnnotatedEcdf(Ecdf):
    def __init__(self, values, input_sensor, output_sensor, gt_sim="Unknown"):
        super().__init__(values)
        if input_sensor is not None and output_sensor is not None:
            self.__legend = f"Execution time between {input_sensor} {output_sensor} {gt_sim}"
            self.__sensors = [input_sensor, output_sensor]
        else:
            self.__legend = ""
            self.__sensors = []
        self.input_sensor = input_sensor
        self.output_sensor = output_sensor
        self.__gt_sim = gt_sim

    # add magic method for sorting
    def __lt__(self, other):
        return self.__legend < other.get_legend()

    def get_label_color(self):
        if self.get_gt_sim() == "gt":
            return "blue"
        else:
            return "orange"

    def plot_cdf(self, legend):
        legend.append(self.get_gt_sim())
        x, y = self.get_cdf_data()

        pyplot.plot(x, y, c=self.get_label_color(), alpha=0.7)
        return legend

    # returns the legend of the eCDF
    def get_legend(self):
        return self.__legend

    # changes the legend of the eCDF
    def set_legend(self, legend):
        self.__legend = legend

    # returns the associated sensors of an Ecdf
    def sensors(self):
        return self.__sensors

    # EV: Add getter for gt_sim
    def get_gt_sim(self):
        return self.__gt_sim

    def as_dict(self):
        return {
            'design': self.get_legend(), 'min': self.get_min_value(), 'max': self.get_max_value(),
            'mean': self.get_avg_value(), 'median': self.get_median_value()
        }


# a collection of Ecdf_s plus a title, e.g., for plotting on the screen or write as image to file
class EcdfCollection:
    def __init__(self, ecdf: AnnotatedEcdf, title=""):
        # EV: Sort the different graphs on the gt_sim value.
        self.__ecdfs = {}
        self.__title = title
        self.__ecdf_conformance_metrics = {}
        self.add_ecdf(ecdf)

    def get_ecdfs(self):
        return self.__ecdfs

    def get_conformance_metrics(self):
        return self.__ecdf_conformance_metrics

    def calculate_conformance_metrics(self, ecdf_1: AnnotatedEcdf, ecdf_2: AnnotatedEcdf):
        conformance_metrics = EcdfConformanceMetrics(ecdf_1, ecdf_2)
        self.__ecdf_conformance_metrics[(ecdf_1.get_legend(), ecdf_2.get_legend())] = conformance_metrics

    def add_ecdf(self, ecdf, compute_conformance_metrics=True):
        if ecdf.get_legend() not in self.__ecdfs:
            if compute_conformance_metrics:
                for prev_ecdf in self.__ecdfs.values():
                    # calculate performance_library metrics for all previous ecdfs (excluding itself)
                    self.calculate_conformance_metrics(prev_ecdf, ecdf)

            self.__ecdfs[ecdf.get_legend()] = ecdf

    def get_ecdfs_to_store(self):
        serialized_ecdfs = []
        for legend, ecdf in self.__ecdfs.items():
            serialized_ecdfs.append({
                "legend": legend,
                "gt_sim": ecdf.get_gt_sim(),
                "serialized_ecdf": ecdf.get_serialized_object(),
                "min": ecdf.get_min_value(),
                "max": ecdf.get_max_value(),
                "average": ecdf.get_avg_value(),
                "median": ecdf.get_median_value()
            })
        return serialized_ecdfs

    def return_title(self):
        return self.__title

    def plot_to_file(self, working_dir, dpi=80, _format="svg", show=False):
        plot = self.plot()
        file_name = working_dir + "/" + self.return_title() + "." + _format
        plot.ioff()
        plot.savefig(file_name, dpi=dpi, format=_format)

        if show:
            plot.show()

    def plot(self):
        pyplot.clf()
        legend = []
        for ecdf in self.__ecdfs.values():
            legend = ecdf.plot_cdf(legend)

        pyplot.legend(legend, loc="lower right", fontsize="6")
        pyplot.title(self.return_title())
        return pyplot

    def get_table_of_ecdf_aggregate(self):
        ecdf_data = [ecdf.as_dict() for ecdf in self.__ecdfs.values()]
        df_ecdf_data = DataFrame(ecdf_data)
        return df_ecdf_data

    def get_conformance_table(self):
        conformance_data = [conformance_metric.as_dict() for conformance_metric in
                            self.__ecdf_conformance_metrics.values()]
        conformance_data = DataFrame(conformance_data)
        return conformance_data
