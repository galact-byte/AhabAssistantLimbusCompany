import tasks.mirror.search_road as road


def test_route_prefers_event_over_battle_with_same_destination():
    graph = road.RouteGraph([], road.Row.MID, (0, 0), hard_mode=True)
    graph._add_new_column()
    graph._add_new_column()
    start = graph.columns["column1"][road.Row.MID]
    event = graph.columns["column2"][road.Row.TOP]
    battle = graph.columns["column2"][road.Row.BOTTOM]
    boss = graph.columns["column3"][road.Row.MID]
    event.node_class, event.weight = "event", road.all_node_weight["event"]
    battle.node_class, battle.weight = "battle", road.all_node_weight["battle"]
    boss.node_class, boss.weight = "boss_battle", road.all_node_weight["boss_battle"]
    start.add_next_node(battle)
    start.add_next_node(event)
    event.add_next_node(boss)
    battle.add_next_node(boss)
    weight, path = graph.find_min_weight_route()
    assert path == [start, event, boss]
    assert weight == start.weight + event.weight + boss.weight


def test_route_without_connections_is_not_fabricated():
    graph = road.RouteGraph([], road.Row.MID, (0, 0), hard_mode=True)
    graph._add_new_column()
    assert graph.find_min_weight_route() == (float("inf"), [])
