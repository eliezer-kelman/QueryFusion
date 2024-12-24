from app.db.database import driver

def execute_neo4j_query(query_id: int, filters: dict = None):
    if query_id == 6:
        return get_expanding_groups()
    if query_id == 7:
        return get_frequent_attackers_by_target()

def get_shared_targets_all_regions():
    with driver.session() as session:
        query = """
        MATCH (:RegionLocation)-[:CONTAINS]->(c:CountryLocation)-[:OCCURRED_IN]->(e:Event)-[:TARGETING]->(tt:TargetType)
        MATCH (e)<-[:RESPONSIBLE_FOR]-(a:Attackers)
        WITH c.country AS country, tt.target_type AS target, a.primary_group AS group
        WITH country, target, COLLECT(DISTINCT group) AS groups
        WHERE SIZE(groups) > 1
        WITH country, COLLECT({target: target, groups: groups}) AS target_groups
        RETURN DISTINCT country, target_groups
        """
        result = session.run(query)
        results = []
        for record in result:
            results.append({
                "country": record["country"],
                "targets": record["target_groups"]
            })
        return results

def get_groups_by_country():
    with driver.session() as session:
        query = """
        MATCH (c:CountryLocation)-[:OCCURRED_IN]->(e:Event)<-[:RESPONSIBLE_FOR]-(a:Attackers)
        WITH c.country AS country, COLLECT(DISTINCT a.primary_group) AS groups
        RETURN country, groups, SIZE(groups) AS group_count
        """
        result = session.run(query)
        countries = []
        for record in result:
            countries.append({
                "country": record["country"],
                "groups": record["groups"],
                "group_count": record["group_count"]
            })
        return countries


def get_attack_strategies_by_country():
    with driver.session() as session:
        query = """
        MATCH (c:CountryLocation)-[:OCCURRED_IN]->(e:Event)-[:OF_TYPE]->(at:AttackType)
        MATCH (e)<-[:RESPONSIBLE_FOR]-(a:Attackers)
        WITH c.country AS country, at.attack_type AS attack_type, COLLECT(DISTINCT a.primary_group) AS groups
        WHERE SIZE(groups) > 1
        RETURN country, attack_type, groups, SIZE(groups) AS group_count
        """
        result = session.run(query)
        strategies = []
        for record in result:
            strategies.append({
                "country": record["country"],
                "attack_type": record["attack_type"],
                "groups": record["groups"],
                "group_count": record["group_count"]
            })
        return strategies


def get_expanding_groups():
    with driver.session() as session:
        query = """
        MATCH (a:Attackers)-[:RESPONSIBLE_FOR]->(e:Event)<-[:OCCURRED_IN]-(c:CountryLocation)
        WITH a.primary_group AS group, e.date AS event_date, c.country AS country
        WITH group, 
             MIN(event_date) AS first_year, 
             MAX(event_date) AS last_year
        MATCH (a)-[:RESPONSIBLE_FOR]->(e:Event)<-[:OCCURRED_IN]-(c:CountryLocation)
        WHERE a.primary_group = group AND (e.date = first_year OR e.date = last_year)
        WITH group, 
             first_year, 
             last_year,
             COLLECT(DISTINCT CASE WHEN e.date = first_year THEN c.country END) AS first_year_countries,
             COLLECT(DISTINCT CASE WHEN e.date = last_year THEN c.country END) AS last_year_countries
        WITH group, 
             first_year, 
             SIZE([country IN first_year_countries WHERE country IS NOT NULL]) AS first_year_country_count,
             last_year, 
             SIZE([country IN last_year_countries WHERE country IS NOT NULL]) AS last_year_country_count
        WHERE last_year_country_count > first_year_country_count
        RETURN group, 
               first_year, 
               first_year_country_count, 
               last_year, 
               last_year_country_count
        """
        result = session.run(query)
        groups = []
        for record in result:
            groups.append({
                "group": record["group"],
                "first_year": str(record["first_year"]),
                "first_year_country_count": record["first_year_country_count"],
                "last_year": str(record["last_year"]),
                "last_year_country_count": record["last_year_country_count"]
            })
        return groups


def get_frequent_attackers_by_target():
    with driver.session() as session:
        query = """
        MATCH (a:Attackers)-[:RESPONSIBLE_FOR]->(e:Event)-[:TARGETING]->(tt:TargetType)
        WITH a.primary_group AS group, tt.target_type AS target_type, COUNT(e) AS attack_count
        WHERE attack_count > 1
        RETURN target_type, COLLECT(group) AS groups
        """
        result = session.run(query)
        targets = []
        for record in result:
            targets.append({
                "target_type": record["target_type"],
                "groups": record["groups"]
            })
        return targets
