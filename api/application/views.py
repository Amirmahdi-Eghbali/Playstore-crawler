import psycopg2
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

connection = psycopg2.connect(
    user='postgres',
    password='AmIrMaHdI',
    host='postgres',
    port=5432
)
cursor = connection.cursor()

class AppIdViewSet(viewsets.ViewSet):
    
    @swagger_auto_schema(
        operation_description="Create a new App",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'app_id': openapi.Schema(type=openapi.TYPE_STRING, description='Unique App ID'),
                'genre': openapi.Schema(type=openapi.TYPE_STRING, description='Genre of the App'),
            },
            required=['app_id', 'genre']
        ),
        responses={
            201: openapi.Response('App created successfully'),
            400: openapi.Response('Bad Request'),
        }
    )
    def create(self, request, *args, **kwargs):
        app_id = request.data.get("app_id")
        genre = request.data.get("genre")

        cursor.execute("SELECT COUNT(*) FROM apps_id WHERE app_id = %s", (app_id,))
        if cursor.fetchone()[0] > 0:
            return Response({"error": "this app already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        cursor.execute("INSERT INTO apps_id (app_id, genre) VALUES (%s, %s)", (app_id, genre))
        connection.commit()
        return Response({"message": "app created successfully"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update an existing App",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the App to update'),
                'app_id': openapi.Schema(type=openapi.TYPE_STRING, description='New App ID'),
                'genre': openapi.Schema(type=openapi.TYPE_STRING, description='New genre for the App'),
            },
        ),
        responses={
            201: openapi.Response('App updated successfully'),
            400: openapi.Response('Bad Request'),
        }
    )
    def update(self, request, *args, **kwargs):
        id = request.data.get("id")
        new_id = request.data.get("app_id")
        new_genre = request.data.get("genre")

        cursor.execute("SELECT id FROM apps_id WHERE app_id = %s", (new_id,))
        current = cursor.fetchone()
        if current and str(current[0]) != str(id):
            return Response({"error": "this app already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        cursor.execute("""
            UPDATE apps_id
            SET app_id = %s, genre = %s
            WHERE id = %s
        """, (new_id, new_genre, id))
        
        connection.commit()
        return Response({"message": "app updated successfully"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="List all Apps",
        responses={200: openapi.Response('A list of all apps')}
    )
    def list(self, request, *args, **kwargs):
        cursor.execute("SELECT * FROM apps_id")
        apps = cursor.fetchall()
        app_list = [{'id': app[0], 'app_id': app[1], 'genre': app[2]} for app in apps]
        return Response(app_list, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        id = request.data.get('id')
        cursor.execute("DELETE FROM apps_id WHERE id = %s", (id,))
        connection.commit()
        return Response({"message": "app deleted successfully"}, status=status.HTTP_202_ACCEPTED)