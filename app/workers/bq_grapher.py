
import os
import time

from networkx import DiGraph
from memory_profiler import profile

from app import APP_ENV
from app.bq_service import BigQueryService
from app.workers import fmt_ts, fmt_n
from app.workers.base_grapher import BaseGrapher

class BigQueryGrapher(BaseGrapher):

    def __init__(self, bq_service=None, gcs_service=None):
        super().__init__(gcs_service=gcs_service)
        self.bq_service = (bq_service or BigQueryService.cautiously_initialized())

    @property
    def metadata(self):
        #meta = super().metadata
        #meta["bq_service"] = self.bq_service.metadata
        #return meta
        return {**super().metadata, **self.bq_service.metadata} # merges dicts

    @profile
    def perform(self):
        self.graph = DiGraph()
        self.running_results = []

        for row in self.bq_service.fetch_user_friends_in_batches():
            self.counter += 1

            if not self.dry_run:
                self.graph.add_edges_from([(row["screen_name"], friend) for friend in row["friend_names"]])

            if self.counter % self.batch_size == 0:
                rr = {"ts": fmt_ts(), "counter": self.counter, "nodes": len(self.graph.nodes), "edges": len(self.graph.edges)}
                print(rr["ts"], "|", fmt_n(rr["counter"]), "|", fmt_n(rr["nodes"]), "|", fmt_n(rr["edges"]))
                self.running_results.append(rr)

if __name__ == "__main__":

    grapher = BigQueryGrapher.cautiously_initialized()
    grapher.write_metadata_to_file()
    grapher.upload_metadata()

    grapher.start()
    grapher.perform()
    grapher.end()
    grapher.report()

    grapher.write_results_to_file()
    grapher.upload_results()

    grapher.write_graph_to_file()
    grapher.upload_graph()

    if APP_ENV == "production":
        print("SLEEPING...")
        time.sleep(12 * 60 * 60) # twelve hours
