class StatsWindowModel:
    def __init__(self, total_time, attentive_percentage, inattentive_percentage, attentive_time, inattentive_time, inattentive_count, qualitative_label):
        self.total_time = total_time
        self.attentive_percentage = attentive_percentage
        self.inattentive_percentage = inattentive_percentage
        self.attentive_time = attentive_time
        self.inattentive_time = inattentive_time
        self.inattentive_count = inattentive_count
        self.qualitative_label = qualitative_label