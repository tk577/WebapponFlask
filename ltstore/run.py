from main.app import app
import main.routes
import main.promotional_routes
import main.catalogue_routes

if __name__ == '__main__':
    app.run(debug=True)