from memory_profiler import profile

from networkx import DiGraph

from app import seek_confirmation
from app.decorators.datetime_decorators import logstamp
from app.decorators.number_decorators import fmt_n
from app.bq_service import BigQueryService
from app.retweet_graphs_v2.graph_storage import GraphStorage
from app.retweet_graphs_v2.job import Job

BOT_MIN = 0.8
BATCH_SIZE = 100


class BotFollowerGrapher(GraphStorage, Job):
    def __init__(self, bq_service=None, bot_min=BOT_MIN, batch_size=BATCH_SIZE, storage_dirpath=None):
        self.bq_service = bq_service or BigQueryService()
        self.bot_min = bot_min
        self.batch_size = batch_size

        Job.__init__(self)

        storage_dirpath = storage_dirpath or f"bot_follower_graphs/bot_min/{self.bot_min}"
        GraphStorage.__init__(self, dirpath=storage_dirpath)

        print("-------------------------")
        print("BOT FOLLOWER GRAPHER...")
        print("  BOT MIN:", self.bot_min)
        print("  BATCH SIZE:", self.batch_size)
        print("-------------------------")

        seek_confirmation()

    @property
    def metadata(self):
        return {**super().metadata, **{"bot_min": self.bot_min, "batch_size": self.batch_size}}

    @profile
    def perform(self):
        self.graph = DiGraph()

        print("FETCHING BOT FOLLOWERS...")

        for row in self.bq_service.fetch_bot_follower_lists(bot_min=self.bot_min):
            bot_id = row["bot_id"]
            self.graph.add_edges_from([(follower_id, bot_id) for follower_id in row["follower_ids"]])

            self.counter += 1
            if self.counter % self.batch_size == 0:
                print("  ", logstamp(), "| BOTS:", fmt_n(self.counter))


if __name__ == "__main__":

    grapher = BotFollowerGrapher()

    grapher.save_metadata()

    grapher.start()
    grapher.perform()
    grapher.end()
    grapher.report()

    grapher.write_graph_to_file()
