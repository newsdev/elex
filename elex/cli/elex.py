from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

class ElexBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'Parse AP election results'
        arguments = [
            ( ['-f', '--foo'],
              dict(action='store', help='the notorious foo option') ),
            ( ['-C'],
              dict(action='store_true', help='the big C option') ),
            ]

    #@expose(hide=True)
    #def default(self):
        #self.app.log.info('Inside MyBaseController.default()')
        #if self.app.pargs.foo:
            #print('Recieved option: foo => %s' % self.app.pargs.foo)

    @expose(help='Get results')
    def get_results(self):
        self.app.log.info('Getting results')


class Elex(CementApp):
    class Meta:
        label = 'elex'
        base_controller = 'base'
        handlers = [ElexBaseController]


def main():
    with Elex() as app:
        app.run()


if __name__ == '__main__':
    main()
