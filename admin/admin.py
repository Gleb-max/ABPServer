from flask_admin.contrib.sqla import ModelView


class ViewWithPK(ModelView):
    column_display_pk = True


class HiddenModelView(ModelView):

    def is_visible(self):
        return False

    def __init__(self, model, session, **kwargs):
        super(HiddenModelView, self).__init__(model, session, **kwargs)
