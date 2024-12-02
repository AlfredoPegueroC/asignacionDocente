from rest_framework.response import Response
from rest_framework import status


def createHandle(request, serializers):
  serializer = serializers(data=request.data)   
  if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def getAllHandle(request, modelData, serializers):
  lista = modelData.objects.all()
  ser = serializers(lista, many=True)
  return Response(ser.data, status=status.HTTP_200_OK)

def updateHandle(request, modelData, serializers, pk):
    try:
        universidad = modelData.objects.get(pk=pk)
    except modelData.DoesNotExist:
        return JsonResponse({'error': 'Universidad not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        ser = serializers(universidad, data=request.data, partial=(request.method == 'PATCH'))
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=status.HTTP_200_OK)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

def deleteHandler(request, pk, modelData):
    try:
        deleteItem= modelData.objects.get(pk=pk)
        deleteItem.delete()  #
        return Response(status=status.HTTP_204_NO_CONTENT)
    except modelData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)