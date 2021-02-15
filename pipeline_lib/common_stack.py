from aws_cdk import (
    core,
    aws_events as events
)


class CommonStack(core.Stack):

    eventbus_arn = None

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ##############################################################################
        #                        Event Bus
        # ##############################################################################

        eventbus = events.EventBus(
            self, "EventBus", event_bus_name=self.node.try_get_context('service_name'))

        self.eventbus_arn = eventbus.event_bus_arn
