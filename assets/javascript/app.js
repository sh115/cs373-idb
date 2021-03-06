var app = angular.module('api2k15', [
    'ngTouch',
    'ui.grid',
    'ui.router',
    'ui.grid.pagination'   
])

.constant('host', 'http://api2k15.me')

.run(function($rootScope, $state) {
    $rootScope.$on('$stateChangeSuccess', function() {
        // scroll to top on page transitions
        $('html, body').animate({ scrollTop: 0 }, 200);
    })
})

.config(function($interpolateProvider, $stateProvider, $urlRouterProvider, $locationProvider) {

    $urlRouterProvider.otherwise('/home');
    $locationProvider.html5Mode(true);

    $stateProvider
        .state('root', {
            url: '',
            abstract: true,
            params: {
                results: null,
                query: null
            },
            views: {
                'navbar': {
                    templateUrl: 'assets/templates/shared/navbar.html',
                    controller: 'NavbarCtrl'
                }
               // 'footer': {
               //     templateUrl: 'assets/templates/shared/footer.html',
               //     controller: 'FooterCtrl'
               // }
            }
        })
        .state('root.home', {
            url: "/home",
            views : { 
                '@' : {
                    templateUrl: "assets/templates/home.html",
                    controller: "HomeCtrl"
                }
            }
        })
        .state('root.teams', {
            url: "/teams",
            views : { 
                '@' : {
                    templateUrl: "assets/templates/teams/teams.html",
                    controller: "TeamsCtrl",
                    resolve: {
                        teams: function(teamFactory, $q, $stateParams) {
                            var deferred = $q.defer();
                            teamFactory.getTeams().then(
                                function(data) {
                                    deferred.resolve(data.data);
                                }, function(error) {
                                    console.log("Can't resolve teams", error);
                                    window.location.href = '/';
                                });
                            return deferred.promise;
                        }
                    }
                }
            }
        })
        .state('root.team-detail', {
            url: "/teams/:id",
            views : {
                '@' : {
                    templateUrl: "assets/templates/teams/team-detail.html",
                    controller: "TeamDetailCtrl",
                    resolve: {
                        team: function(teamFactory, $q, $stateParams) {
                            var deferred = $q.defer();
                            teamFactory.getTeamDetail($stateParams['id']).then(
                                function(data) {
                                    deferred.resolve(data.data);
                                }, function(error) {
                                    console.log("Can't resolve team details", error);
                                    window.location.href = '/';
                                });
                            return deferred.promise;
                        }
                    }
                }
            }
        })
        .state('root.players', {
            url: "/players",
            views : { 
                '@' : {
                    templateUrl: "assets/templates/players/players.html",
                    controller: "PlayersCtrl",
                    resolve: {
                        players: function(playerFactory, $q, $stateParams) {
                            var deferred = $q.defer();
                            playerFactory.getPlayers().then(
                                function(data) {
                                    deferred.resolve(data.data);
                                }, function(error) {
                                    console.log("Can't resolve players", error);
                                    window.location.href = '/';
                                });
                            return deferred.promise;
                        }
                    }
                }
            }
        })
        .state('root.player-detail', {
            url: "/player/:id",
            views : {
                '@' : {
                    templateUrl: "assets/templates/players/player-detail.html",
                    controller: "PlayerDetailCtrl",
                    resolve: {
                        player: function(playerFactory, $q, $stateParams) {
                            var deferred = $q.defer();
                            playerFactory.getPlayerDetail($stateParams['id']).then(
                                function(data) {
                                    deferred.resolve(data.data);
                                }, function(error) {
                                    console.log("Can't resolve player details", error);
                                    window.location.href = '/';
                                });
                            return deferred.promise;
                        }
                    }
                }
            }
        })
        .state('root.games', {
            url: "/games",
            views : { 
                '@' : {
                    templateUrl: "assets/templates/games/games.html",
                    controller: "GamesCtrl",
                    resolve: {
                        games: function(gameFactory, $q, $stateParams) {
                            var deferred = $q.defer();
                            gameFactory.getGames().then(
                                function(data) {
                                    deferred.resolve(data.data);
                                }, function(error) {
                                    console.log("Can't resolve games", error);
                                    window.location.href = '/';
                                });
                            return deferred.promise;
                        }
                    }
                }
            }
        })
        .state('root.game-detail', {
            url: "/game/:id",
            views : {
                '@' : {
                    templateUrl: "assets/templates/games/game-detail.html",
                    controller: "GameDetailCtrl",
                    resolve: {
                        game: function(gameFactory, $q, $stateParams) {
                            var deferred = $q.defer();
                            gameFactory.getGameDetail($stateParams['id']).then(
                                function(data) {
                                    deferred.resolve(data.data);
                                }, function(error) {
                                    console.log("Can't resolve game details", error);
                                    window.location.href = '/';
                                });
                            return deferred.promise;
                        }
                    }
                }
            }
        })
        .state('root.search', {
            url: "/search",
            views: {
                '@' : {
                    templateUrl: 'assets/templates/search/search.html',
                    controller: 'SearchCtrl'
                }
            }
        })
        .state('root.whoweighsmore', {
            url: "/whoweighsmore",
            views: {
                '@' : {
                    templateUrl: 'assets/templates/otherAPI/otherAPI.html',
                    controller: 'OtherAPICtrl',
                    resolve: {
                        bplayer: function(otherFactory, $q) {
                            var deferred = $q.defer();
                            otherFactory.getBPlayer().then(
                                function(data) {
                                    deferred.resolve(data.data);
                                }, function(error) {
                                    console.log("Can't resolve player details", error);
                                    window.location.href = '/';
                                });
                            return deferred.promise;
                        },
                        fplayer: function(otherFactory, $q) {
                            var deferred = $q.defer();
                            otherFactory.getFPlayer().then(
                                function(data) {
                                    deferred.resolve(data.data);
                                }, function(error) {
                                    console.log("Can't resolve player details", error);
                                    window.location.href = '/';
                                });
                            return deferred.promise;
                        }
                    }
                }
            }
        })
        .state('root.about', {
            url: "/about",
            views : { 
                '@' : {
                    templateUrl: "assets/templates/about/about.html",
                    controller: "AboutCtrl"
                }
            }
        });
});
