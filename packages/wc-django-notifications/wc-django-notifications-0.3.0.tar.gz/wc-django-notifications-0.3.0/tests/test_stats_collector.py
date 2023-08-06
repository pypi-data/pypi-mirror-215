import pytest
from pprint import pprint

from wcd_notifications.services import notifier, manager
from wcd_notifications.models.notifications import Notification
from wcd_notifications.contrib.drf.views import stats_list_view
from wcd_notifications.signals import notifications_sent, notifications_updated

from .utils import mute_signals


@pytest.mark.django_db
def test_stats_collect_mechanics(rf, make_user, django_assert_num_queries):
    user, _ = make_user('1')
    user2, _ = make_user('2')

    with mute_signals(notifications_sent, notifications_updated):
        notifications = notifier.send(
            'Found some {actor} for you {recipient}', [user, user2],
            actor=user,
            flags=[Notification.Readability.UNREAD],
        )
        notifications += notifier.send(
            'Found some {actor} for you {recipient}', [user],
            actor=user2,
            flags=[Notification.Readability.UNREAD],
        )
        notifications += notifier.send(
            'Found some {actor} for you {recipient}', [user],
            actor=user,
            flags=[Notification.Readability.READ],
        )

    with django_assert_num_queries(4):
        stat, = manager.collect_stats([user])

    assert stat.total == 3
    assert stat.flags[Notification.Readability.UNREAD] == 2
    assert stat.flags[Notification.Readability.READ] == 1

    with django_assert_num_queries(4):
        stat2, = manager.collect_stats([user])

    assert stat.pk == stat2.pk


@pytest.mark.django_db
def test_stats_view(rf, make_user, django_assert_num_queries):
    user, _ = make_user('1')
    user2, _ = make_user('2')

    with mute_signals(notifications_sent, notifications_updated):
        notifications = notifier.send(
            'Found some {actor} for you {recipient}', [user, user2],
            actor=user,
            flags=[Notification.Readability.UNREAD],
        )
        notifications += notifier.send(
            'Found some {actor} for you {recipient}', [user],
            actor=user2,
            flags=[Notification.Readability.UNREAD],
        )
    notifications += notifier.send(
        'Found some {actor} for you {recipient}', [user],
        actor=user,
        flags=[Notification.Readability.READ],
    )

    request = rf.get('/stats/')
    request.user = user
    response = stats_list_view(request)

    assert response.status_code == 200
    assert len(response.data) == 1

    stat = response.data[0]

    assert stat['recipient']['id'] == user.pk
    assert stat['total'] == 3
    assert stat['flags'][str(Notification.Readability.UNREAD)] == 2
    assert stat['flags'][str(Notification.Readability.READ)] == 1
