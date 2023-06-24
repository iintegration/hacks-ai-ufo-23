module meta {
  abstract type Created {
    created: datetime {
      rewrite insert using (datetime_of_statement())
    }
  }

  abstract type Modified {
    modified: datetime {
      rewrite update using (datetime_of_statement())
    }
  }
}

module default {
  type Subject extending meta::Created, meta::Modified {
    required obj_key: str;
    state: str;
    square: str;
    general_designer_key: str;
    general_contractor: str;
    number_of_workers: int64;
    type: str;
    subtype: str;
    multi link tasks := .<subject[is Task];
  }

  type Task extending meta::Created, meta::Modified {
    required subject: Subject;
    required name: str;
    required code: str;
    predicted_end_date: datetime;
    actual_end_date: datetime;
    multi link reasons := .<task[is Reason];
  }

  type Reason extending meta::Created, meta::Modified {
    required name: str;
    required about: str;
    required task: Task;
  }

  type User extending meta::Created, meta::Modified {
    required login: str {
      constraint exclusive;
    }
    required password_hash: str;
    multi link tokens := .<owner[is Token]
  }

  type Token extending meta::Created, meta::Modified {
    required owner: User;
    required value: str {
      constraint exclusive;
    }
  }

  type File extending meta::Created, meta::Modified {
    required owner: User;
    required origin_filename: str;
    required obj_key: str;
  }
}
